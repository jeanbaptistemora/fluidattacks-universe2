{ nixpkgs
, path
, ...
}:
let
  terraformApply = import (path "/makes/utils/terraform-apply") path nixpkgs;
in
terraformApply {
  name = "makes-aws-sso-apply";
  product = "makes";
  target = "makes/applications/makes/aws-sso/src/terraform";
}
