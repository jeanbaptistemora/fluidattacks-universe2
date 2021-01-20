{ observesPkgsTerraform
, path
, ...
} @ _:
let
  terraformTest = import (path "/makes/utils/bash-lib/terraform-test") path observesPkgsTerraform;
in
terraformTest {
  name = "observes-infra-test";
  product = "observes";
  target = "observes/infra/terraform";
}
