{ nixpkgs
, path
, ...
}:
let
  terraformTest = import (path "/makes/utils/terraform-test") path nixpkgs;
in
terraformTest {
  name = "serves-users-sorts-test";
  product = "serves";
  target = "makes/applications/serves/users/sorts/src/terraform";
}
