{ makesPkgs
, terraformApply
, ...
} @ _:
terraformApply makesPkgs {
  name = "makes-docs-infra-apply";
  product = "serves";
  target = "makes/applications/makes/docs/infra/terraform";
  secretsPath = "serves/secrets/development.yaml";
}
