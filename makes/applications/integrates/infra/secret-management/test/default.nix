{ terraformTest
, ...
}:
terraformTest {
  name = "integrates-infra-secret-management-test";
  product = "integrates";
  target = "integrates/deploy/secret-management/terraform";
}
