module "cache" {
  source  = "npalm/gitlab-runner/aws//modules/cache"
  version = "5.9.1"

  environment                    = "common-ci-cache"
  cache_bucket_versioning        = false
  cache_expiration_days          = 30
  cache_lifecycle_clear          = true
  cache_bucket_set_random_suffix = true

  cache_bucket_name_include_account_id = false
  cache_lifecycle_prefix               = "common-ci-cache"
  cache_bucket_prefix                  = "common-ci-cache"

  tags = {
    "Name"               = "common-ci-cache"
    "management:area"    = "innovation"
    "management:product" = "common"
    "management:type"    = "product"
  }
}
