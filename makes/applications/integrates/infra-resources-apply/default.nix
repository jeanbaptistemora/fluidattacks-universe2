{ path
, integratesPkgsTerraform
, ...
} @ _:
let
  terraformApply = import (path "/makes/utils/terraform-apply") path integratesPkgsTerraform;
in
terraformApply {
  name = "integrates-infra-resources-apply";
  product = "integrates";
  target = "integrates/deploy/terraform-resources";
}
