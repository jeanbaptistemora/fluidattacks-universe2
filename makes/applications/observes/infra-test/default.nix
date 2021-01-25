{ observesPkgsTerraform
, path
, ...
} @ _:
let
  terraformTest = import (path "/makes/utils/terraform-test") path observesPkgsTerraform;
in
terraformTest {
  name = "observes-infra-test";
  product = "observes";
  target = "observes/infra/terraform";
}
