attrs @ {
  pkgsSkimsTerraform,
  ...
}:

let
  terraformApply = import ../../../makes/utils/bash-lib/terraform-apply pkgsSkimsTerraform;
in
  terraformApply {
    name = "skims-infra-deploy";
    path = "skims/infra";
    product = "skims";
  }
