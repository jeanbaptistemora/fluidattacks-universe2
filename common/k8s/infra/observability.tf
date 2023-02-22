variable "datadogApiKey" {}
variable "newRelicLicenseKey" {}

resource "helm_release" "newrelic" {
  name       = "newrelic"
  repository = "https://helm-charts.newrelic.com"
  chart      = "nri-bundle"
  version    = "5.0.4"
  namespace  = "kube-system"

  values = [
    yamlencode(
      {
        global = {
          cluster = local.cluster_name
        }
        newrelic-infrastructure = {
          privileged = true
        }
        kube-state-metrics = {
          enabled = true
        }
        nri-kube-events = {
          enabled = true
        }
        newrelic-logging = {
          enabled = true
        }
      }
    )
  ]

  set_sensitive {
    name  = "global.licenseKey"
    value = var.newRelicLicenseKey
  }
}

resource "helm_release" "datadog" {
  name            = "datadog-agent"
  namespace       = "kube-system"
  repository      = "https://helm.datadoghq.com"
  chart           = "datadog"
  version         = "3.10.9"
  atomic          = true
  cleanup_on_fail = true

  values = [
    yamlencode(
      {
        agents = {
          affinity = {
            nodeAffinity = {
              requiredDuringSchedulingIgnoredDuringExecution = {
                nodeSelectorTerms = [
                  {
                    matchExpressions = [
                      {
                        key      = "worker-group"
                        operator = "In"
                        values   = ["prod-integrates"]
                      }
                    ]
                  }
                ]
              }

            }
          }
        },
        clusterAgent = {
          affinity = {
            nodeAffinity = {
              requiredDuringSchedulingIgnoredDuringExecution = {
                nodeSelectorTerms = [
                  {
                    matchExpressions = [
                      {
                        key      = "worker-group"
                        operator = "In"
                        values   = ["prod-integrates"]
                      }
                    ]
                  }
                ]
              }

            }
          }
        }
      }
    )
  ]

  set_sensitive {
    name  = "datadog.apiKey"
    value = var.datadogApiKey
  }
}
