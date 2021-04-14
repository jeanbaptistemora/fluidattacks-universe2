{ terraformTest
, ...
}:
terraformTest {
  name = "docs-infra-test";
  product = "makes";
  target = "docs/infra/terraform";
  secretsPath = "makes/applications/makes/secrets/src/development.yaml";
}
