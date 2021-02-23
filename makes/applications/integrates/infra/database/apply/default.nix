{ path
, integratesPkgsTerraform
, ...
}:
let
  terraformApply = import (path "/makes/utils/terraform-apply") path integratesPkgsTerraform;
in
terraformApply {
  name = "integrates-infra-database-apply";
  product = "integrates";
  target = "integrates/deploy/database/terraform";
}
