resource "helm_release" "metrics_server" {
  name       = "metrics-server"
  repository = "https://kubernetes-sigs.github.io/metrics-server"
  chart      = "metrics-server"
  version    = "3.5.0"
  namespace  = "kube-system"

  set {
    name  = "replicas"
    value = 3
  }
}
