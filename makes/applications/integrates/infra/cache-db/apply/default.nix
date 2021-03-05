{ terraformApply
, ...
}:
terraformApply {
  name = "integrates-infra-cache-db-apply";
  product = "integrates";
  target = "integrates/deploy/cache-db/terraform";
}
