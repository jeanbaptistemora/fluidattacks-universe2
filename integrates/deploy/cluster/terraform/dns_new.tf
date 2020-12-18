resource "kubernetes_deployment" "cloudflare_external_dns" {
  metadata {
    name      = "cloudflare-external-dns"
    namespace = "kube-system"
    labels = {
      "app.kubernetes.io/name"       = "cloudflare-external-dns"
      "app.kubernetes.io/version"    = "v${var.external_dns_version}"
      "app.kubernetes.io/managed-by" = "terraform"
    }
  }

  spec {
    replicas = 1

    selector {
      match_labels = {
        "app.kubernetes.io/name" = "cloudflare-external-dns"
      }
    }

    strategy {
      type = "Recreate"
    }

    template {
      metadata {
        labels = {
          "app.kubernetes.io/name"    = "cloudflare-external-dns"
          "app.kubernetes.io/version" = var.external_dns_version
        }
      }

      spec {
        container {
          name              = "cloudflare-external-dns"
          image             = "k8s.gcr.io/external-dns/external-dns:v0.7.3"
          image_pull_policy = "Always"

          args = [
            "--source=service",
            "--source=ingress",
            "--domain-filter=fluidattacks.com",
            "--provider=cloudflare",
            "--policy=sync",
            "--registry=txt",
            "--txt-owner-id=cloudflare-external-dns",
            "--cloudflare-proxied",
          ]

          env {
            name  = "CF_API_TOKEN"
            value = var.cloudflare_api_token
          }
        }
      }
    }
  }
}
