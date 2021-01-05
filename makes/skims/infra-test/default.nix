_ @ {
  skimsPkgsTerraform,
  ...
}:

let
  terraformTest = import ../../../makes/utils/bash-lib/terraform-test skimsPkgsTerraform;
in
  terraformTest {
    name = "skims-infra-test";
    path = "skims/infra";
    product = "skims";
  }
