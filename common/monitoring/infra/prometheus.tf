locals {
  namespace = "kube-system"
  role_name = "monitoring"
  tags = {
    "Name"               = "prometheus"
    "management:area"    = "cost"
    "management:product" = "common"
    "management:type"    = "product"
  }
}

data "aws_caller_identity" "current" {}

data "aws_eks_cluster" "k8s_cluster" {
  name = "common-k8s"
}

data "aws_subnet" "k8s_subnets" { # common/vpc/infra/subnets.tf
  count = 3
  filter {
    name   = "tag:Name"
    values = ["k8s_${count.index + 1}"]
  }
}

resource "aws_vpc_endpoint" "prometheus_endpoint" {
  service_name = "com.amazonaws.us-east-1.aps-workspaces"
  vpc_id       = data.aws_subnet.k8s_subnets[0].vpc_id
  subnet_ids = [
    for subnet in data.aws_subnet.k8s_subnets : subnet.id
  ]
  vpc_endpoint_type = "Interface"
  tags              = local.tags
}

resource "aws_prometheus_workspace" "monitoring" {
  alias = "common-monitoring"
  tags  = local.tags

  logging_configuration {
    log_group_arn = "${aws_cloudwatch_log_group.monitoring.arn}:*"
  }
}

resource "helm_release" "cert_manager" {
  name            = "cert-manager"
  description     = "Certificate manager, required to install OpenTelemtry Operator"
  repository      = "https://charts.jetstack.io"
  chart           = "cert-manager"
  version         = "1.11.0"
  namespace       = local.namespace
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
  namespace       = local.namespace
  cleanup_on_fail = true
  atomic          = true

  depends_on = [
    helm_release.cert_manager
  ]
}

data "aws_iam_policy_document" "prometheus_permissions" {
  statement {
    actions = [
      "aps:GetLabels",
      "aps:GetMetricMetadata",
      "aps:GetSeries",
      "aps:RemoteWrite"
    ]
    resources = [
      aws_prometheus_workspace.monitoring.arn
    ]
  }
}

data "aws_iam_policy_document" "k8s_oidc" {
  statement {
    actions = ["sts:AssumeRoleWithWebIdentity"]

    condition {
      test     = "StringEquals"
      values   = ["system:serviceaccount:${local.namespace}:${local.role_name}"]
      variable = "${replace(data.aws_eks_cluster.k8s_cluster.identity[0].oidc[0].issuer, "https://", "")}:sub"
    }

    principals {
      type        = "Federated"
      identifiers = ["arn:aws:iam::${data.aws_caller_identity.current.account_id}:oidc-provider/${replace(data.aws_eks_cluster.k8s_cluster.identity[0].oidc[0].issuer, "https://", "")}"]
    }
  }
}

resource "aws_iam_policy" "prometheus" {
  name        = "EKSPrometheusAccess"
  description = "Permissions required for ADOT Collector to send scraped metrics to AMP"
  policy      = data.aws_iam_policy_document.prometheus_permissions.json
}

resource "aws_iam_role" "monitoring" {
  name               = local.role_name
  assume_role_policy = data.aws_iam_policy_document.k8s_oidc.json
}

resource "aws_iam_role_policy_attachment" "prometheus_access" {
  role       = aws_iam_role.monitoring.name
  policy_arn = aws_iam_policy.prometheus.arn
}

resource "kubernetes_service_account" "monitoring" {
  automount_service_account_token = true
  metadata {
    name      = local.role_name
    namespace = local.namespace

    annotations = {
      "eks.amazonaws.com/role-arn" = aws_iam_role.monitoring.arn
    }
  }
}

resource "kubernetes_cluster_role" "monitoring" {
  metadata {
    name = local.role_name
  }

  rule {
    api_groups = [""]
    resources = [
      "endpoints",
      "nodes",
      "nodes/metrics",
      "nodes/proxy",
      "pods",
      "services"
    ]
    verbs = [
      "get",
      "list",
      "watch"
    ]
  }

  rule {
    non_resource_urls = ["/metrics"]
    verbs             = ["get"]
  }
}

resource "kubernetes_cluster_role_binding" "monitoring" {
  metadata {
    name = local.role_name
  }

  role_ref {
    api_group = "rbac.authorization.k8s.io"
    kind      = "ClusterRole"
    name      = kubernetes_cluster_role.monitoring.metadata[0].name
  }

  subject {
    kind      = "ServiceAccount"
    name      = kubernetes_service_account.monitoring.metadata[0].name
    namespace = local.namespace
  }
}

resource "kubernetes_manifest" "adot_collector" {
  manifest = {
    apiVersion = "opentelemetry.io/v1alpha1"
    kind       = "OpenTelemetryCollector"
    metadata = {
      name      = "adot-collector"
      namespace = local.namespace
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

        hostmetrics:
          collection_interval: 10s
          scrapers:
            paging:
              metrics:
                system.paging.utilization:
                  enabled: true
            cpu:
              metrics:
                system.cpu.utilization:
                  enabled: true
            disk:
            filesystem:
              metrics:
                system.filesystem.utilization:
                  enabled: true
            load:
            memory:
            network:

        processors:
          k8sattributes:
          batch:
            send_batch_max_size: 100
            send_batch_size: 10
            timeout: 10s

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
          statsd:

        exporters:
          datadog:
            api:
              site: datadoghq.com
              key: ${var.datadogApiKey}
          prometheusremotewrite:
            endpoint: https://aps-workspaces.us-east-1.amazonaws.com/workspaces/ws-e60ff23e-bccf-4df2-bf46-745c50b45c70/api/v1/remote_write
            auth:
              authenticator: sigv4auth

        service:
          extensions: [sigv4auth]
          pipelines:
            metrics:
              receivers: [hostmetrics, otlp, prometheus, statsd]
              processors: [k8sattributes, batch]
              exporters: [datadog, prometheusremotewrite]
            traces:
              receivers: [otlp]
              processors: [k8sattributes, batch]
              exporters: [datadog]
      EOT
    }
  }

  depends_on = [
    helm_release.adot_operator,
    kubernetes_service_account.monitoring
  ]
}

# For some reason, installing node-exporter from the Helm Chart
# https://artifacthub.io/packages/helm/prometheus-community/prometheus-node-exporter
# does not work, metrics are not sent to Prometheus and there is no error shown
resource "kubernetes_daemon_set_v1" "node_exporter" {
  metadata {
    name      = "node-exporter"
    namespace = local.namespace
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
                  values = [
                    "dev",
                    "prod_integrates"
                  ]
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
    namespace = local.namespace
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
