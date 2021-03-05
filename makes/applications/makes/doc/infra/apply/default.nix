{ terraformApply
, ...
}:
terraformApply {
  name = "makes-doc-infra-apply";
  product = "serves";
  target = "makes/applications/makes/doc/infra/terraform";
  secretsPath = "serves/secrets/development.yaml";
}
