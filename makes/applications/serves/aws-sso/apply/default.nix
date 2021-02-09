{ servesPkgsTerraform
, path
, ...
} @ _:
let
  terraformApply = import (path "/makes/utils/terraform-apply") path servesPkgsTerraform;
in
terraformApply {
  name = "serves-aws-sso-apply";
  product = "serves";
  target = "serves/aws-sso/terraform";
}
