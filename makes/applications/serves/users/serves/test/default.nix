{ servesPkgs
, path
, ...
} @ _:
let
  terraformTest = import (path "/makes/utils/terraform-test") path servesPkgs;
in
terraformTest {
  name = "serves-users-serves-test";
  product = "serves";
  target = "serves/users/serves/terraform";
}
