{ terraformTest
, ...
}:
terraformTest {
  name = "integrates-infra-cache-db-test";
  product = "integrates";
  target = "integrates/deploy/cache-db/terraform";
}
