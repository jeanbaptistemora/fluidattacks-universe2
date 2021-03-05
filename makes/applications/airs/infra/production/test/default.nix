{ terraformTest
, ...
}:
terraformTest {
  name = "airs-infra-production-test";
  product = "airs";
  target = "airs/deploy/production/terraform";
  secretsPath = "airs/deploy/secret-management/development.yaml";
}
