variable "ci_cache_access_key" {
  default = "default value for test"
}
variable "ci_cache_secret_key" {
  default = "default value for test"
}
variable "ci_registration_token" {
  default = "default value for test"
}
variable "ci_registration_token_autonomic" {
  default = "default value for test"
}

data "local_file" "ci_init" {
  filename = "ci-init.sh"
}
data "local_file" "ci_config" {
  filename = "ci-config.yaml"
}
data "local_file" "ci_config_autonomic" {
  filename = "ci-config-autonomic.yaml"
}
data "local_file" "ci_config_large" {
  filename = "ci-config-large.yaml"
}

resource "aws_s3_bucket" "cache_bucket" {
  bucket        = "ci-cache.fluidattacks.com"
  acl           = "private"
  force_destroy = true

  versioning {
    enabled = false
  }

  server_side_encryption_configuration {
    rule {
      apply_server_side_encryption_by_default {
        sse_algorithm = "AES256"
      }
    }
  }

  tags = {
    "Name"               = "ci-cache.fluidattacks.com"
    "management:type"    = "production"
    "management:product" = "makes"
  }
}

resource "kubernetes_secret" "cache_creds" {
  metadata {
    name      = "ci-cache-creds"
    namespace = "ci"
  }

  data = {
    accesskey = var.ci_cache_access_key
    secretkey = var.ci_cache_secret_key
  }

  type = "Opaque"
}

resource "kubernetes_secret" "registration_token" {
  metadata {
    name      = "ci-registration-token"
    namespace = "ci"
  }

  data = {
    "runner-registration-token" = var.ci_registration_token
    "runner-token"              = ""
  }

  type = "Opaque"
}

resource "kubernetes_secret" "registration_token_autonomic" {
  metadata {
    name      = "ci-registration-token-autonomic"
    namespace = "ci"
  }

  data = {
    "runner-registration-token" = var.ci_registration_token_autonomic
    "runner-token"              = ""
  }

  type = "Opaque"
}

resource "helm_release" "ci" {
  name       = "ci"
  repository = "https://charts.gitlab.io"
  chart      = "gitlab-runner"
  version    = "0.27.0-rc1"
  namespace  = "ci"

  values = [
    data.local_file.ci_config.content
  ]
}

resource "helm_release" "ci_autonomic" {
  name       = "ci-autonomic"
  repository = "https://charts.gitlab.io"
  chart      = "gitlab-runner"
  version    = "0.27.0-rc1"
  namespace  = "ci"

  values = [
    data.local_file.ci_config_autonomic.content
  ]
}

resource "helm_release" "ci_large" {
  name       = "ci-large"
  repository = "https://charts.gitlab.io"
  chart      = "gitlab-runner"
  version    = "0.27.0-rc1"
  namespace  = "ci"

  values = [
    data.local_file.ci_config_large.content
  ]
}
