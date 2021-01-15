{ observesPkgsTerraform
, ...
} @ _:
let
  terraformTest = import ../../../makes/utils/bash-lib/terraform-test observesPkgsTerraform;
in
terraformTest {
  name = "observes-infra-test";
  path = "observes/infra/terraform";
  product = "observes";
}
