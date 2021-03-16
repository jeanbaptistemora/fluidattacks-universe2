{ nixpkgs
, path
, ...
}:
let
  terraformTest = import (path "/makes/utils/terraform-test") path nixpkgs;
in
terraformTest {
  name = "serves-users-melts-test";
  product = "serves";
  target = "makes/applications/serves/users/melts/src/terraform";
}
