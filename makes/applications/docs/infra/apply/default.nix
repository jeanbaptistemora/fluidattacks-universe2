{ terraformApply
, ...
}:
terraformApply {
  name = "docs-infra-apply";
  product = "docs";
  target = "docs/infra/terraform";
  secretsPath = "docs/secrets/prod.yaml";
}
