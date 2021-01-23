{ path
, skimsPkgsTerraform
, ...
} @ _:
let
  terraformApply = import (path "/makes/utils/terraform-apply") path skimsPkgsTerraform;
in
terraformApply {
  name = "skims-infra-deploy";
  product = "skims";
  target = "skims/infra";
}
