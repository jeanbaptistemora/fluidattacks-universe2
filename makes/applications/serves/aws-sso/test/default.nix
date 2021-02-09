{ servesPkgsTerraform
, path
, ...
} @ _:
let
  terraformTest = import (path "/makes/utils/terraform-test") path servesPkgsTerraform;
in
terraformTest {
  name = "serves-aws-sso-test";
  product = "serves";
  target = "serves/aws-sso/terraform";
}
