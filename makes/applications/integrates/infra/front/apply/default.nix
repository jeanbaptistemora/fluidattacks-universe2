{ terraformApply
, ...
}:
terraformApply {
  name = "integrates-infra-front-apply";
  product = "integrates";
  secretsPath = "integrates/secrets-production.yaml";
  target = "integrates/deploy/front/terraform";
}
