{ nixpkgs
, path
, ...
}:
let
  terraformTest = import (path "/makes/utils/terraform-test") path nixpkgs;
in
terraformTest {
  name = "makes-users-skims-test";
  product = "makes";
  target = "makes/applications/makes/users/skims/src/terraform";
}
