variable "gitlabTokenFluidattacks" {}

resource "helm_release" "ci_small" {
  chart       = "gitlab-runner"
  description = "Kubernetes Event Driven Autoscaler"
  name        = "ci-small"
  namespace   = "dev"
  repository  = "https://charts.gitlab.io/"
  version     = "0.49.1"

  values = [
    yamlencode(
      {
        imagePullPolicy               = "IfNotPresent"
        replicas                      = 5
        gitlabUrl                     = "https://gitlab.com/"
        unregisterRunners             = true
        terminationGracePeriodSeconds = 86400
        concurrent                    = 1000
        checkInterval                 = 5
        logLevel                      = "info"
        rbac = {
          create            = true
          clusterWideAccess = true
        }
        metrics = {
          enabled : true
        }
        securityContext = {
          runAsUser = 100
          fsGroup   = 65533
        }
        resources = {
          requests = {
            memory = "2500Mi"
            cpu    = "1200m"
          }
        }
        nodeSelector = {
          worker_group = "ci"
        }
        runners = {
          executor    = "kubernetes"
          locked      = true
          tags        = "ci"
          runUntagged = true
          protected   = false
          config      = <<-EOF
          [[runners]]
            name = "ci"
            environment = ["FF_GITLAB_REGISTRY_HELPER_IMAGE=true", "FF_USE_LEGACY_KUBERNETES_EXECUTION_STRATEGY=false"]
            request_concurrency = 10
            output_limit = 16384

            [runners.kubernetes]
              cpu_request = "1200m"
              memory_request = "2500Mi"
              helper_cpu_request = "1m"
              helper_memory_request = "1Mi"
              namespace = "dev"
              poll_timeout = 300
              privileged = false
              allow_privilege_escalation = false
              [runners.kubernetes.node_selector]
                worker_group = "ci"
              [dns_config]
                nameservers = ["1.1.1.1", "8.8.4.4", "8.8.8.8"]
        EOF
        }
      }
    )
  ]

  set_sensitive {
    name  = "runnerRegistrationToken"
    value = var.gitlabTokenFluidattacks
  }
}
