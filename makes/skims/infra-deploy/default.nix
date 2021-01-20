{ path
, skimsPkgsTerraform
, ...
} @ _:
let
  terraformApply = import (path "/makes/utils/bash-lib/terraform-apply") skimsPkgsTerraform;
in
terraformApply {
  name = "skims-infra-deploy";
  path = "skims/infra";
  product = "skims";
}
