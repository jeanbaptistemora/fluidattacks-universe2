{ servesPkgsTerraform
, path
, ...
} @ _:
let
  terraformTest = import (path "/makes/utils/terraform-test") path servesPkgsTerraform;
in
terraformTest {
  name = "serves-test-user-provision-forces";
  product = "serves";
  target = "serves/services/user-provision/forces/terraform";
}
