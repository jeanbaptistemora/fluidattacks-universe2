{ terraformApply
, ...
}:
terraformApply {
  name = "makes-doc-infra-apply";
  product = "makes";
  target = "makes/applications/makes/doc/infra/terraform";
  secretsPath = "makes/applications/makes/secrets/src/development.yaml";
}
