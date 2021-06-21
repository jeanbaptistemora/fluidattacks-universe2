{ terraformApply
, ...
}:
terraformApply {
  name = "integrates-infra-secret-management-apply";
  product = "integrates";
  target = "integrates/deploy/secret-management/terraform";
}
