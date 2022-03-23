resource "helm_release" "kubecost" {
  name       = "kubecost"
  repository = "https://kubecost.github.io/cost-analyzer/"
  chart      = "cost-analyzer"
  version    = "1.91.2"
  namespace  = "kubecost"

  set {
    name  = "kubecostToken"
    value = var.kubecostToken
  }
}
