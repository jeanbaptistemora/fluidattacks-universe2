{ terraformApply
, ...
}:
terraformApply {
  name = "makes-okta-apply";
  product = "makes";
  target = "makes/applications/makes/okta/src/terraform";
  secretsPath = "makes/applications/makes/okta/src/terraform/data.yaml";
}
