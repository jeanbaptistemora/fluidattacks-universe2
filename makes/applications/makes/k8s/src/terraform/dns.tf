resource "kubernetes_service_account" "external_dns_cloudflare" {
  automount_service_account_token = true
  metadata {
    name      = "external-dns-cloudflare"
    namespace = "kube-system"
    labels = {
      "app.kubernetes.io/name"       = "external-dns-cloudflare"
      "app.kubernetes.io/managed-by" = "terraform"
    }
  }
}

resource "kubernetes_cluster_role" "external_dns_cloudflare" {
  metadata {
    name = "external-dns-cloudflare"
    labels = {
      "app.kubernetes.io/name"       = "external-dns-cloudflare"
      "app.kubernetes.io/managed-by" = "terraform"
    }
  }

  rule {
    api_groups = [
      "",
    ]
    resources = [
      "endpoints",
      "pods",
      "services",
    ]
    verbs = [
      "get",
      "list",
      "watch",
    ]
  }
  rule {
    api_groups = [
      "extensions",
      "networking.k8s.io",
    ]
    resources = [
      "ingresses",
    ]
    verbs = [
      "get",
      "list",
      "watch",
    ]
  }
  rule {
    api_groups = [
      "",
    ]
    resources = [
      "nodes",
    ]
    verbs = [
      "list",
      "watch",
    ]
  }
}

resource "kubernetes_cluster_role_binding" "external_dns_cloudflare" {
  metadata {
    name = "external-dns-cloudflare"
    labels = {
      "app.kubernetes.io/name"       = "external-dns-cloudflare"
      "app.kubernetes.io/managed-by" = "terraform"
    }
  }

  role_ref {
    api_group = "rbac.authorization.k8s.io"
    kind      = "ClusterRole"
    name      = kubernetes_cluster_role.external_dns_cloudflare.metadata[0].name
  }

  subject {
    api_group = ""
    kind      = "ServiceAccount"
    name      = kubernetes_service_account.external_dns_cloudflare.metadata[0].name
    namespace = kubernetes_service_account.external_dns_cloudflare.metadata[0].namespace
  }
}

resource "kubernetes_deployment" "external_dns_cloudflare" {
  metadata {
    name      = "external-dns-cloudflare"
    namespace = "kube-system"
    labels = {
      "app.kubernetes.io/name"       = "external-dns-cloudflare"
      "app.kubernetes.io/version"    = "v${var.external_dns_version}"
      "app.kubernetes.io/managed-by" = "terraform"
    }
  }

  spec {
    replicas = 1

    selector {
      match_labels = {
        "app.kubernetes.io/name" = "external-dns-cloudflare"
      }
    }

    strategy {
      type = "Recreate"
    }

    template {
      metadata {
        labels = {
          "app.kubernetes.io/name"    = "external-dns-cloudflare"
          "app.kubernetes.io/version" = var.external_dns_version
        }
      }

      spec {
        automount_service_account_token = true
        service_account_name            = kubernetes_service_account.external_dns_cloudflare.metadata[0].name

        container {
          name              = "external-dns-cloudflare"
          image             = "k8s.gcr.io/external-dns/external-dns:v0.7.3"
          image_pull_policy = "Always"

          args = [
            "--source=service",
            "--source=ingress",
            "--domain-filter=fluidattacks.com",
            "--provider=cloudflare",
            "--policy=sync",
            "--registry=txt",
            "--txt-owner-id=external-dns-cloudflare",
            "--cloudflare-proxied",
          ]

          env {
            name  = "CF_API_EMAIL"
            value = var.cloudflare_email
          }
          env {
            name  = "CF_API_KEY"
            value = var.cloudflare_api_key
          }
        }
      }
    }
  }
}
