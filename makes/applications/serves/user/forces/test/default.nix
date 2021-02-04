{ servesPkgsTerraform
, path
, ...
} @ _:
let
  terraformTest = import (path "/makes/utils/terraform-test") path servesPkgsTerraform;
in
terraformTest {
  name = "serves-user-forces-test";
  product = "serves";
  target = "serves/services/user-provision/forces/terraform";
}
