{ terraformApply
, ...
}:
terraformApply {
  name = "integrates-infra-backup-apply";
  product = "integrates";
  target = "integrates/deploy/backup/terraform";
}
