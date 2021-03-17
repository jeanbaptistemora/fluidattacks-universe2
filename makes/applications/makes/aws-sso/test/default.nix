{ nixpkgs
, path
, ...
}:
let
  terraformTest = import (path "/makes/utils/terraform-test") path nixpkgs;
in
terraformTest {
  name = "makes-aws-sso-test";
  product = "makes";
  target = "makes/applications/makes/aws-sso/src/terraform";
}
