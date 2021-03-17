{ nixpkgs
, path
, ...
}:
let
  terraformTest = import (path "/makes/utils/terraform-test") path nixpkgs;
in
terraformTest {
  name = "makes-users-melts-test";
  product = "makes";
  target = "makes/applications/makes/users/melts/src/terraform";
}
