resource "helm_release" "dns" {
  name       = "dns"
  repository = "https://charts.bitnami.com/bitnami"
  chart      = "external-dns"
  version    = "6.5.6"
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
    value = "common-cluster"
  }

  set {
    name  = "txtPrefix"
    value = "common-cluster"
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
