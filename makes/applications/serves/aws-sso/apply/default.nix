{ nixpkgs
, path
, ...
}:
let
  terraformApply = import (path "/makes/utils/terraform-apply") path nixpkgs;
in
terraformApply {
  name = "serves-aws-sso-apply";
  product = "serves";
  target = "serves/aws-sso/terraform";
}
