variable "gitlabRunnerToken" {}

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

locals {
  ci = {
    small = {
      name          = "ci-small"
      replicas      = 1
      node_selector = module.cluster.eks_managed_node_groups.ci_small.node_group_labels.worker_group
      requests = {
        cpu    = "1200m"
        memory = "2500Mi"
      }
      tags = ["small"]
    }
    large = {
      name          = "ci-large"
      replicas      = 1
      node_selector = module.cluster.eks_managed_node_groups.ci_large.node_group_labels.worker_group
      requests = {
        cpu    = "1200m"
        memory = "4000Mi"
      }
      tags = ["large"]
    }
  }
}

resource "helm_release" "ci" {
  for_each = local.ci

  chart       = "gitlab-runner"
  description = "Kubernetes Event Driven Autoscaler"
  name        = each.value.name
  namespace   = "dev"
  repository  = "https://charts.gitlab.io/"
  version     = "0.49.2"

  values = [
    yamlencode(
      {
        imagePullPolicy               = "IfNotPresent"
        replicas                      = "${each.value.replicas}"
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
          worker_group = local.ci.small.node_selector
        }
        runners = {
          executor       = "kubernetes"
          locked         = true
          tags           = "${join(",", each.value.tags)}"
          runUntagged    = false
          protected      = false
          maximumTimeout = "86400"
          config         = <<-EOF
            [[runners]]
              name = "${each.value.name}"
              request_concurrency = 10
              output_limit = 16384

              [runners.kubernetes]
                pull_policy = "always"
                cpu_request = "${each.value.requests.cpu}"
                memory_request = "${each.value.requests.memory}"
                helper_cpu_request = "1m"
                helper_memory_request = "1Mi"
                namespace = "dev"
                poll_timeout = 600
                privileged = true
                [runners.kubernetes.node_selector]
                  worker_group = "${each.value.node_selector}"
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
    value = var.gitlabRunnerToken
  }
}
