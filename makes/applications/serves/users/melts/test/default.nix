{ servesPkgs
, path
, ...
} @ _:
let
  terraformTest = import (path "/makes/utils/terraform-test") path servesPkgs;
in
terraformTest {
  name = "serves-users-melts-test";
  product = "serves";
  target = "serves/users/melts/terraform";
}
