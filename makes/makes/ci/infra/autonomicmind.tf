module "autonomicmind_ci_cache" {
  source  = "npalm/gitlab-runner/aws//modules/cache"
  version = "4.28.0"

  environment             = "autonomicmind-ci-cache"
  cache_bucket_versioning = false
  cache_expiration_days   = 30
  cache_lifecycle_clear   = true
  cache_lifecycle_prefix  = ""
  create_cache_bucket     = true

  tags = {
    "management:type"    = "production"
    "management:product" = "makes"
  }
}
