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
