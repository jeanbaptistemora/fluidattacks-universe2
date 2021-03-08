{ terraformTest
, ...
}:
terraformTest {
  name = "integrates-infra-front-test";
  product = "integrates";
  secretsPath = "integrates/secrets-development.yaml";
  target = "integrates/deploy/front/terraform";
}
