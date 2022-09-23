# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

variable "ciGitlabApiToken" {}
variable "ciGitlabSshKey" {}
variable "ciUsers" {}

locals {
  values = {
    controller = {
      # Plugins
      installPlugins = [
        "configuration-as-code:1512.vb_79d418d5fc8",
        "git:4.11.5",
        "gitlab-plugin:1.5.35",
        "kubernetes:3706.vdfb_d599579f3",
        "workflow-aggregator:590.v6a_d052e5a_a_b_5",
      ]

      # Security
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
        configScripts = {
          gitlab = yamlencode({
            credentials = {
              system = {
                domainCredentials = [
                  {
                    credentials = [
                      {
                        gitLabApiTokenImpl = {
                          scope       = "SYSTEM"
                          id          = "ci_gitlab_token"
                          apiToken    = var.ciGitlabApiToken
                          description = "CI Gitlab Token"
                        }
                      },
                      {
                        basicSSHUserPrivateKey = {
                          scope       = "GLOBAL"
                          id          = "ci_gitlab_ssh_key"
                          username    = ""
                          passphrase  = ""
                          description = "SSH key for GitLab Git operations."
                          privateKeySource = {
                            directEntry = {
                              privateKey = var.ciGitlabSshKey
                            }
                          }
                        }
                      },
                    ]
                  }
                ]
              }
            }
            unclassified = {
              gitlabconnectionconfig = {
                connections = [
                  {
                    apiTokenId              = "ci_gitlab_token"
                    clientBuilderId         = "autodetect"
                    connectionTimeout       = 20
                    ignoreCertificateErrors = true
                    name                    = "gitlab"
                    readTimeout             = 10
                    url                     = "https://gitlab.com/"
                  }
                ]
              }
            }
          })
        }
      }

      # Network
      serviceType = "NodePort"
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
