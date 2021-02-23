{ servesPkgs
, path
, ...
}:
let
  terraformApply = import (path "/makes/utils/terraform-apply") path servesPkgs;
in
terraformApply {
  name = "serves-aws-sso-apply";
  product = "serves";
  target = "serves/aws-sso/terraform";
}
