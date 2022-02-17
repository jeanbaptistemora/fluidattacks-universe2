variable "dynatraceApiToken" {}
variable "dynatraceApiUrl" {}
variable "dynatracePaasToken" {}

resource "helm_release" "dynatrace" {
  name       = "dynatrace"
  repository = "https://raw.githubusercontent.com/Dynatrace/helm-charts/master/repos/stable"
  chart      = "dynatrace-operator"
  version    = "0.4.1"
  namespace  = "kube-system"

  set_sensitive {
    name  = "apiToken"
    value = var.dynatraceApiToken
  }

  set_sensitive {
    name  = "apiUrl"
    value = var.dynatraceApiUrl
  }

  set_sensitive {
    name  = "paasToken"
    value = var.dynatracePaasToken
  }

  set {
    name  = "classicFullStack.enabled"
    value = true
  }

  set {
    name  = "name"
    value = var.cluster_name
  }

  set {
    name  = "activeGate.capabilities"
    value = yamlencode(["routing", "kubernetes-monitoring"])
  }
}
