{ path
, integratesPkgsTerraform
, ...
}:
let
  envTerraformApply = import (path "/makes/utils/terraform-apply") path integratesPkgsTerraform;
in
envTerraformApply {
  name = "integrates-infra-backup-apply";
  product = "integrates";
  target = "integrates/deploy/backup/terraform";
}
