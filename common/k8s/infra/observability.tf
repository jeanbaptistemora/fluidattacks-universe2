variable "datadogApiKey" {}

resource "helm_release" "datadog" {
  name            = "datadog-agent"
  namespace       = "kube-system"
  repository      = "https://helm.datadoghq.com"
  chart           = "datadog"
  version         = "3.10.9"
  atomic          = true
  cleanup_on_fail = true

  // https://github.com/DataDog/helm-charts/blob/main/charts/datadog/values.yaml
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
                        key      = "worker_group"
                        operator = "In"
                        values   = ["prod_integrates"]
                      }
                    ]
                  }
                ]
              }
            }
          }
        }
        clusterAgent = {
          affinity = {
            nodeAffinity = {
              requiredDuringSchedulingIgnoredDuringExecution = {
                nodeSelectorTerms = [
                  {
                    matchExpressions = [
                      {
                        key      = "worker_group"
                        operator = "In"
                        values   = ["prod_integrates"]
                      }
                    ]
                  }
                ]
              }
            }
          }
        }
        datadog = {
          apm = {
            portEnabled = true
          }
          dogstatsd = {
            nonLocalTraffic = true
            port            = 8135
            useHostPort     = true
          }
          otlp = {
            receiver = {
              protocols = {
                grpc = {
                  enabled  = true
                  endpoint = "0.0.0.0:4327"
                }
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
