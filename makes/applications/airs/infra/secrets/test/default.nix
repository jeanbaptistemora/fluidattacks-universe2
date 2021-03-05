{ terraformTest
, ...
}:
terraformTest {
  name = "airs-infra-secrets-test";
  product = "airs";
  target = "airs/deploy/secret-management/terraform";
}
