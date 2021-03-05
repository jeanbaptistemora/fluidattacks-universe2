{ nixpkgs
, path
, ...
}:
let
  terraformTest = import (path "/makes/utils/terraform-test") path nixpkgs;
in
terraformTest {
  name = "serves-users-skims-test";
  product = "serves";
  target = "serves/users/skims/terraform";
}
