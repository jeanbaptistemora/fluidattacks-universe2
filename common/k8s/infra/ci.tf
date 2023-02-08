variable "gitlabTokenFluidattacks" {}

module "ci_cache" {
  source  = "npalm/gitlab-runner/aws//modules/cache"
  version = "5.9.1"

  environment                          = "${local.cluster_name}-ci-cache"
  cache_bucket_set_random_suffix       = true
  cache_bucket_name_include_account_id = false

  cache_bucket_versioning = false
  cache_expiration_days   = 30
  cache_lifecycle_clear   = true

  tags = {
    "Name"               = "${local.cluster_name}-ci-cache"
    "management:area"    = "innovation"
    "management:product" = "common"
    "management:type"    = "product"
  }
}

resource "helm_release" "ci_small" {
  chart       = "gitlab-runner"
  description = "Kubernetes Event Driven Autoscaler"
  name        = "ci-small"
  namespace   = "dev"
  repository  = "https://charts.gitlab.io/"
  version     = "0.49.1"

  values = [
    yamlencode(
      {
        imagePullPolicy               = "IfNotPresent"
        replicas                      = 1
        gitlabUrl                     = "https://gitlab.com/"
        unregisterRunners             = true
        terminationGracePeriodSeconds = 86400
        concurrent                    = 1000
        checkInterval                 = 5
        logLevel                      = "info"
        rbac = {
          create            = true
          clusterWideAccess = true
        }
        metrics = {
          enabled = true
        }
        securityContext = {
          allowPrivilegeEscalation = false
          readOnlyRootFilesystem   = false
          runAsNonRoot             = true
          privileged               = false
        }
        resources = {
          requests = {
            memory = "2500Mi"
            cpu    = "1200m"
          }
        }
        nodeSelector = {
          worker_group = "ci"
        }
        runners = {
          executor    = "kubernetes"
          locked      = true
          tags        = "ci"
          runUntagged = true
          protected   = false
          config      = <<-EOF
            [[runners]]
              name = "ci"
              request_concurrency = 10
              output_limit = 16384

              [runners.kubernetes]
                cpu_request = "1200m"
                memory_request = "2500Mi"
                helper_cpu_request = "1m"
                helper_memory_request = "1Mi"
                namespace = "dev"
                poll_timeout = 300
                privileged = false
                allow_privilege_escalation = false
                [runners.kubernetes.node_selector]
                  worker_group = "ci"
                [dns_config]
                  nameservers = ["1.1.1.1", "8.8.8.8", "8.8.4.4"]

              [runners.cache]
                Type = "s3"
                Shared = true
                [runners.cache.s3]
                  AuthenticationType = "iam"
                  ServerAddress = "s3.amazonaws.com"
                  BucketName = "${module.ci_cache.bucket}"
                  BucketLocation = "us-east-1"
                  Insecure = false
          EOF
        }
      }
    )
  ]

  set_sensitive {
    name  = "runnerRegistrationToken"
    value = var.gitlabTokenFluidattacks
  }
}
