{ nixpkgs
, path
, ...
}:
let
  terraformTest = import (path "/makes/utils/terraform-test") path nixpkgs;
in
terraformTest {
  name = "makes-users-forces-test";
  product = "makes";
  target = "makes/applications/makes/users/forces/src/terraform";
}
