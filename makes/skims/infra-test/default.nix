{ path
, skimsPkgsTerraform
, ...
} @ _:
let
  terraformTest = import (path "/makes/utils/bash-lib/terraform-test") skimsPkgsTerraform;
in
terraformTest {
  name = "skims-infra-test";
  path = "skims/infra";
  product = "skims";
}
