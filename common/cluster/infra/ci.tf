# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

variable "ciUsers" {}

locals {
  values = {
    controller = {
      JCasC = {
        securityRealm = yamlencode({
          local = {
            allowsSignup  = false
            enableCaptcha = false
            users         = jsondecode(var.ciUsers)
          }
        })
        authorizationStrategy = yamlencode({
          loggedInUsersCanDoAnything = {
            allowAnonymousRead = false
          }
        })
      }
      ingress = {
        enabled    = true
        apiVersion = "extensions/v1beta1"
        hostName   = "ci.fluidattacks.com"
        annotations = {
          "kubernetes.io/ingress.class"                         = "alb"
          "alb.ingress.kubernetes.io/scheme"                    = "internet-facing"
          "alb.ingress.kubernetes.io/tags"                      = "management:area=cost,management:product=common,management:type=product"
          "alb.ingress.kubernetes.io/load-balancer-attributes"  = "idle_timeout.timeout_seconds=120"
          "alb.ingress.kubernetes.io/security-groups"           = "CloudFlare"
          "alb.ingress.kubernetes.io/healthcheck-path"          = "/"
          "alb.ingress.kubernetes.io/success-codes"             = "200,302"
          "alb.ingress.kubernetes.io/unhealthy-threshold-count" = "6"
          "alb.ingress.kubernetes.io/listen-ports"              = "[{\"HTTP\": 80}]"
          "external-dns.alpha.kubernetes.io/cloudflare-proxied" = "true"
        }
      }
      serviceType = "NodePort"
    }
  }
}

resource "helm_release" "ci" {
  name       = "ci"
  repository = "https://charts.jenkins.io"
  chart      = "jenkins"
  version    = "4.2.5"
  namespace  = "kube-system"
  values     = [yamlencode(local.values)]
}
