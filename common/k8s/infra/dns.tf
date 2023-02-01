variable "cloudflareEmail" {}
variable "cloudflareApiKey" {}

resource "helm_release" "dns" {
  name       = "dns"
  repository = "https://charts.bitnami.com/bitnami"
  chart      = "external-dns"
  version    = "6.13.1"
  namespace  = "kube-system"

  set {
    name  = "provider"
    value = "cloudflare"
  }

  set {
    name  = "policy"
    value = "sync"
  }

  set {
    name  = "registry"
    value = "txt"
  }

  set {
    name  = "txtOwnerId"
    value = local.cluster_name
  }

  set {
    name  = "txtPrefix"
    value = "${local.cluster_name}-"
  }

  set {
    name  = "cloudflare.proxied"
    value = true
  }

  set {
    name  = "cloudflare.email"
    value = var.cloudflareEmail
  }

  set {
    name  = "cloudflare.apiKey"
    value = var.cloudflareApiKey
  }
}
