{ servesPkgs
, path
, ...
}:
let
  terraformTest = import (path "/makes/utils/terraform-test") path servesPkgs;
in
terraformTest {
  name = "serves-aws-sso-test";
  product = "serves";
  target = "serves/aws-sso/terraform";
}
