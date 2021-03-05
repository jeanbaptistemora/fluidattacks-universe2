{ terraformTest
, ...
}:
terraformTest {
  name = "integrates-infra-database-test";
  product = "integrates";
  target = "integrates/deploy/database/terraform";
}
