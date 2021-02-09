{ servesPkgsTerraform
, path
, ...
} @ _:
let
  terraformTest = import (path "/makes/utils/terraform-test") path servesPkgsTerraform;
in
terraformTest {
  name = "serves-users-forces-test";
  product = "serves";
  target = "serves/users/forces/terraform";
}
