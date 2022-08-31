module "cache" {
  source  = "npalm/gitlab-runner/aws//modules/cache"
  version = "5.1.0"

  environment                    = "common-ci-cache"
  cache_bucket_versioning        = false
  cache_expiration_days          = 30
  cache_lifecycle_clear          = true
  create_cache_bucket            = true
  cache_bucket_set_random_suffix = true

  cache_bucket_name_include_account_id = false
  cache_lifecycle_prefix               = "common-ci-cache"
  cache_bucket_prefix                  = "common-ci-cache"

  tags = {
    "Name"               = "common-ci-cache"
    "Management:Area"    = "innovation"
    "Management:Product" = "common"
    "Management:Type"    = "product"
  }
}
