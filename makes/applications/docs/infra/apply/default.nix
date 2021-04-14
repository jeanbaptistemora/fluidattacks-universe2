{ terraformApply
, ...
}:
terraformApply {
  name = "docs-infra-apply";
  product = "makes";
  target = "docs/infra/terraform";
  secretsPath = "makes/applications/makes/secrets/src/development.yaml";
}
