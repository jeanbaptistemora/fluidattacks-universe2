{ makesPkgs
, terraformTest
, ...
} @ _:
terraformTest makesPkgs {
  name = "makes-docs-infra-test";
  product = "serves";
  target = "makes/applications/makes/docs/infra/terraform";
  secretsPath = "serves/secrets/development.yaml";
}
