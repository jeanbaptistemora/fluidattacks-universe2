{ servesPkgs
, path
, ...
}:
let
  terraformTest = import (path "/makes/utils/terraform-test") path servesPkgs;
in
terraformTest {
  name = "serves-users-forces-test";
  product = "serves";
  target = "serves/users/forces/terraform";
}
