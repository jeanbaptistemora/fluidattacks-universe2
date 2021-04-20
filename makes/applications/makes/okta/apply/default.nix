{ nixpkgs
, path
, ...
}:
let
  terraformApply = import (path "/makes/utils/terraform-apply") path nixpkgs;
in
terraformApply {
  name = "makes-okta-apply";
  product = "makes";
  target = "makes/applications/makes/okta/src/terraform";
}
