{ terraformTest
, ...
}:
terraformTest {
  name = "docs-infra-test";
  product = "docs";
  target = "docs/infra/terraform";
  secretsPath = "docs/secrets/dev.yaml";
}
