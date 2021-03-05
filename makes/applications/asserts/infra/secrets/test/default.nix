{ terraformTest
, ...
}:
terraformTest {
  name = "asserts-infra-secrets-test";
  product = "asserts";
  target = "asserts/deploy/secret-management/terraform";
}
