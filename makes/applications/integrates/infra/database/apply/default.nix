{ terraformApply
, ...
}:
terraformApply {
  name = "integrates-infra-database-apply";
  product = "integrates";
  target = "integrates/deploy/database/terraform";
}
