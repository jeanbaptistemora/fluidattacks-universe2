attrs @ {
  pkgsSkimsTerraform,
  ...
}:

let
  terraformTest = import ../../../makes/utils/bash-lib/terraform-test pkgsSkimsTerraform;
in
  terraformTest {
    name = "skims-infra-test";
    path = "skims/infra";
    product = "skims";
  }
