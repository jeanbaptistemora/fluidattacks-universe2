{ path
, skimsPkgsTerraform
, ...
} @ _:
let
  terraformTest = import (path "/makes/utils/bash-lib/terraform-test") path skimsPkgsTerraform;
in
terraformTest {
  name = "skims-infra-test";
  product = "skims";
  target = "skims/infra";
}
