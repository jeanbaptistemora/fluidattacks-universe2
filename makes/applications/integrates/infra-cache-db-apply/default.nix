{ path
, integratesPkgsTerraform
, ...
} @ _:
let
  terraformApply = import (path "/makes/utils/terraform-apply") path integratesPkgsTerraform;
in
terraformApply {
  name = "integrates-infra-cache-db-apply";
  product = "integrates";
  target = "integrates/deploy/cache-db/terraform";
}
