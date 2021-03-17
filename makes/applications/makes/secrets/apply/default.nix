{ nixpkgs
, path
, ...
}:
let
  terraformApply = import (path "/makes/utils/terraform-apply") path nixpkgs;
in
terraformApply {
  name = "makes-secrets-apply";
  product = "makes";
  target = "makes/applications/makes/secrets/src/terraform";
}
