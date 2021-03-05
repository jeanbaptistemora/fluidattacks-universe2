{ terraformTest
, ...
}:
terraformTest {
  name = "airs-infra-ephemeral-test";
  product = "airs";
  target = "airs/deploy/ephemeral/terraform";
  secretsPath = "airs/deploy/secret-management/development.yaml";
}
