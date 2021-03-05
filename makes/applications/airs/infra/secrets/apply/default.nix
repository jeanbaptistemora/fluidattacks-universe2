{ terraformApply
, ...
}:
terraformApply {
  name = "airs-infra-secrets-apply";
  product = "airs";
  target = "airs/deploy/secret-management/terraform";
}
