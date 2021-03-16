{ nixpkgs
, path
, ...
}:
let
  terraformTest = import (path "/makes/utils/terraform-test") path nixpkgs;
in
terraformTest {
  name = "serves-aws-sso-test";
  product = "serves";
  target = "makes/applications/serves/aws-sso/src/terraform";
}
