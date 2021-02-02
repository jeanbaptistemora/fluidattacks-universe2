{ path
, integratesPkgsTerraform
, ...
} @ _:
let
  terraformApply = import (path "/makes/utils/terraform-apply") path integratesPkgsTerraform;
in
terraformApply {
  name = "integrates-infra-secret-management-apply";
  product = "integrates";
  target = "integrates/deploy/secret-management/terraform";
}
