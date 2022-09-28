# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

variable "ciGitlabApiToken" {}
variable "ciGitlabSshKey" {}

locals {
  values = {
    # Worker resources
    agent = {
      podName = "ci-worker"
      resources = {
        requests = {
          cpu    = "1200m"
          memory = "3500Mi"
        }
        limits = {
          cpu    = "2000m"
          memory = "3800Mi"
        }
      }
    }
    controller = {
      # Plugins
      installPlugins = [
        "blueocean:1.25.8",
        "configuration-as-code:1512.vb_79d418d5fc8",
        "git:4.11.5",
        "gitlab-plugin:1.5.35",
        "job-dsl:1.81",
        "kubernetes:3706.vdfb_d599579f3",
        "pipeline-stage-view:2.24",
        "saml:4.354.vdc8c005cda_34",
        "workflow-aggregator:590.v6a_d052e5a_a_b_5",
      ]

      # Jenkins Configuration as Code
      JCasC = {
        security = {
          gitHostKeyVerificationConfiguration = {
            sshHostKeyVerificationStrategy = {
              manuallyProvidedKeyVerificationStrategy = {
                approvedHostKeys = <<-EOF
                  github.com ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIOMqqnkVzrm0SdG6UOoqKLsabgH5C9okWi0dh2l9GKJl
                  gitlab.com ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIAfuCHKVTjquxvt6CM6tdG4SLp1Btn/nOeHHE5UOzRdf
                  bitbucket.org ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIOMqqnkVzrm0SdG6UOoqKLsabgH5C9okWi0dh2l9GKJl
                EOF
              }
            }
          }
        }
        securityRealm = yamlencode({
          saml = {
            binding                  = "urn:oasis:names:tc:SAML:2.0:bindings:HTTP-Redirect"
            displayNameAttributeName = "displayname"
            emailAttributeName       = "email"
            groupsAttributeName      = "group"
            idpMetadataConfiguration = {
              period = 0
              url    = "https://fluidattacks.okta.com/app/exkm1ndoheeYZ1Sdj357/sso/saml/metadata"
            }
            maximumAuthenticationLifetime = 86400
            usernameAttributeName         = "username"
            usernameCaseConversion        = "none"
            logoutUrl                     = "https://fluidattacks.okta.com"
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
            jobs = [
              {
                script = <<-EOF
                  multibranchPipelineJob('universe') {
                    branchSources {
                      git {
                        id = 'universe'
                        remote('git@gitlab.com:fluidattacks/universe.git')
                        credentialsId('ci_gitlab_ssh_key')
                      }
                    }
                  }
                EOF
              }
            ]
          })
        }
      }

      # Network
      serviceType        = "NodePort"
      jenkinsUrlProtocol = "https"
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
