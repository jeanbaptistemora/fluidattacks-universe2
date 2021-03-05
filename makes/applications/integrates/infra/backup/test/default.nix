{ terraformTest
, ...
}:
terraformTest {
  name = "integrates-infra-backup-test";
  product = "integrates";
  target = "integrates/deploy/backup/terraform";
}
