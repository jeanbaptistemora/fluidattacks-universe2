{ terraformApply
, ...
}:
terraformApply {
  name = "makes-doc-infra-apply";
  product = "makes";
  target = "docs/infra/terraform";
  secretsPath = "makes/applications/makes/secrets/src/development.yaml";
}
