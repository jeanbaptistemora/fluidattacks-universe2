{ path
, skimsPkgsTerraform
, ...
}:
let
  terraformTest = import (path "/makes/utils/terraform-test") path skimsPkgsTerraform;
in
terraformTest {
  name = "skims-infra-test";
  product = "skims";
  target = "skims/infra";
}
