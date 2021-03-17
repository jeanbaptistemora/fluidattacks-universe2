{ nixpkgs
, path
, ...
}:
let
  terraformTest = import (path "/makes/utils/terraform-test") path nixpkgs;
in
terraformTest {
  name = "makes-users-services-test";
  product = "makes";
  target = "makes/applications/makes/users/services/src/terraform";
}
