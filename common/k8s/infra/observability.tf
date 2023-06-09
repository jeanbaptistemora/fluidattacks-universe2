locals {
  kube_namespace = "kube-system"
}

# For some reason, installing node-exporter from the Helm Chart
# https://artifacthub.io/packages/helm/prometheus-community/prometheus-node-exporter
# does not work, metrics are not sent to Prometheus and there is no error shown
resource "kubernetes_daemon_set_v1" "node_exporter" {
  metadata {
    name      = "node-exporter"
    namespace = local.kube_namespace
    labels = {
      app = "node-exporter"
    }
  }

  spec {
    selector {
      match_labels = {
        app = "node-exporter"
      }
    }

    template {
      metadata {
        labels = {
          app = "node-exporter"
        }
      }

      spec {
        host_network = true

        affinity {
          node_affinity {
            required_during_scheduling_ignored_during_execution {
              node_selector_term {
                match_expressions {
                  key      = "worker_group"
                  operator = "In"
                  values   = local.users
                }
              }
            }
          }
        }

        container {
          args = [
            "--path.sysfs=/host/sys",
            "--path.rootfs=/host/root",
            "--no-collector.wifi",
            "--no-collector.hwmon",
            "--collector.filesystem.ignored-mount-points=^/(dev|proc|sys|var/lib/docker/.+|var/lib/kubelet/pods/.+)($|/)",
            "--collector.netclass.ignored-devices=^(veth.*)$"
          ]
          name  = "node-exporter"
          image = "prom/node-exporter:v1.5.0"

          port {
            container_port = 9100
            host_port      = 9100
            protocol       = "TCP"
          }

          resources {
            limits = {
              cpu    = "250m"
              memory = "180Mi"
            }
            requests = {
              cpu    = "102m"
              memory = "180Mi"
            }
          }

          volume_mount {
            mount_path        = "/host/sys"
            mount_propagation = "HostToContainer"
            name              = "sys"
            read_only         = true
          }
          volume_mount {
            mount_path        = "/host/root"
            mount_propagation = "HostToContainer"
            name              = "root"
            read_only         = true
          }
        }

        volume {
          name = "sys"
          host_path {
            path = "/sys"
          }
        }
        volume {
          name = "root"
          host_path {
            path = "/"
          }
        }
      }
    }
  }
}

resource "kubernetes_service_v1" "node_exporter_service" {
  metadata {
    name      = "node-exporter"
    namespace = local.kube_namespace
    annotations = {
      "prometheus.io/scrape" = "true"
      "prometheus.io/port"   = "9100"
    }
  }

  spec {
    selector = {
      app = "node-exporter"
    }

    port {
      port        = 9100
      target_port = 9100
      protocol    = "TCP"
    }
  }
}

resource "helm_release" "cert_manager" {
  name            = "cert-manager"
  description     = "Certificate manager, required to install OpenTelemtry Operator"
  repository      = "https://charts.jetstack.io"
  chart           = "cert-manager"
  version         = "1.11.0"
  namespace       = local.kube_namespace
  cleanup_on_fail = true
  atomic          = true

  set {
    name  = "installCRDs"
    value = "true"
  }
}

resource "helm_release" "adot_operator" {
  name            = "adot-operator"
  description     = "OpenTelemetry Operator, scrapes metrics and sends them to AWS Managed Prometheus"
  repository      = "https://open-telemetry.github.io/opentelemetry-helm-charts"
  chart           = "opentelemetry-operator"
  version         = "0.21.2"
  namespace       = local.kube_namespace
  cleanup_on_fail = true
  atomic          = true

  depends_on = [
    helm_release.cert_manager
  ]
}

resource "kubernetes_manifest" "adot_collector" {
  manifest = {
    apiVersion = "opentelemetry.io/v1alpha1"
    kind       = "OpenTelemetryCollector"
    metadata = {
      name      = "adot-collector"
      namespace = local.kube_namespace
    }
    spec = {
      image          = "public.ecr.aws/aws-observability/aws-otel-collector:v0.26.0"
      mode           = "deployment"
      serviceAccount = kubernetes_service_account.monitoring.metadata[0].name
      config         = <<EOT
        extensions:
          sigv4auth:
            service: "aps"
            region: "us-east-1"

        processors:
          batch:

        receivers:
          otlp:
            protocols:
              grpc:
          prometheus:
            config:
              scrape_configs:
                - job_name: 'kubernetes-nodes'
                  scheme: https

                  kubernetes_sd_configs:
                    - role: node

                  relabel_configs:
                    - action: labelmap
                      regex: __meta_kubernetes_node_label_(worker_group)
                      replacement: aws_$$${1}

                    - action: labelmap
                      regex: __meta_kubernetes_node_label_node_kubernetes_io_(instance_type)
                      replacement: aws_$$${1}

                  tls_config:
                    ca_file: /var/run/secrets/kubernetes.io/serviceaccount/ca.crt
                    insecure_skip_verify: true
                  bearer_token_file: /var/run/secrets/kubernetes.io/serviceaccount/token

                - job_name: 'kubernetes-cadvisor'
                  scheme: https
                  metrics_path: /metrics/cadvisor

                  kubernetes_sd_configs:
                    - role: node

                  relabel_configs:
                    - action: labelmap
                      regex: __meta_kubernetes_node_label_(worker_group)
                      replacement: aws_$$${1}

                    - action: labelmap
                      regex: __meta_kubernetes_node_label_node_kubernetes_io_(instance_type)
                      replacement: aws_$$${1}

                  tls_config:
                    ca_file: /var/run/secrets/kubernetes.io/serviceaccount/ca.crt
                    insecure_skip_verify: true
                  bearer_token_file: /var/run/secrets/kubernetes.io/serviceaccount/token

                - job_name: 'kubernetes-node-exporter'
                  scheme: http

                  kubernetes_sd_configs:
                    - role: endpoints

                  relabel_configs:
                    - source_labels: [__meta_kubernetes_endpoints_name]
                      regex: 'node-exporter'
                      action: keep
                    - source_labels: [__meta_kubernetes_pod_node_name]
                      action: replace
                      target_label: instance

                - job_name: 'kubernetes-arm'
                  scheme: http

                  kubernetes_sd_configs:
                    - role: endpoints

                  relabel_configs:
                    - source_labels: [__meta_kubernetes_service_name]
                      action: keep
                      regex: integrates-trunk
                    - source_labels: [__meta_kubernetes_service_name]
                      action: replace
                      target_label: service_name

          statsd:

        exporters:
          awsxray:
            indexed_attributes: ["graphql.operation.name", "otel.resource.deployment.environment"]
            region: "us-east-1"
          prometheusremotewrite:
            endpoint: https://aps-workspaces.us-east-1.amazonaws.com/workspaces/ws-e60ff23e-bccf-4df2-bf46-745c50b45c70/api/v1/remote_write
            auth:
              authenticator: sigv4auth

        service:
          extensions: [sigv4auth]
          pipelines:
            metrics:
              receivers: [otlp, prometheus, statsd]
              processors: [batch]
              exporters: [prometheusremotewrite]
            traces:
              receivers: [otlp]
              processors: [batch]
              exporters: [awsxray]
      EOT
    }
  }

  depends_on = [helm_release.adot_operator]
}

resource "kubernetes_service_v1" "adot_collector_service" {
  metadata {
    name      = "adot-collector"
    namespace = local.kube_namespace
  }

  spec {
    selector = {
      "app.kubernetes.io/name" = "adot-collector-collector"
    }

    port {
      name        = "grpc-port"
      port        = 4317
      target_port = 4317
      protocol    = "TCP"
    }

    port {
      name        = "statsd-port"
      port        = 8125
      target_port = 8125
      protocol    = "UDP"
    }
  }

  depends_on = [
    kubernetes_manifest.adot_collector
  ]
}
