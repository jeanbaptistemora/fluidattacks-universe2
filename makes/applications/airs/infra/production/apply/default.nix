{ terraformApply
, ...
}:
terraformApply {
  name = "airs-infra-production-apply";
  product = "airs";
  target = "airs/deploy/production/terraform";
  secretsPath = "airs/deploy/secret-management/production.yaml";
}
