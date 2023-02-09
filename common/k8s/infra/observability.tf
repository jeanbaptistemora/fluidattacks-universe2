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
