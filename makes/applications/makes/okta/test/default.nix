{ nixpkgs
, path
, ...
}:
let
  terraformTest = import (path "/makes/utils/terraform-test") path nixpkgs;
in
terraformTest {
  name = "makes-okta-test";
  product = "makes";
  target = "makes/applications/makes/okta/src/terraform";
}
