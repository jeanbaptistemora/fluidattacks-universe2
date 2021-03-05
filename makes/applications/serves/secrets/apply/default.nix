{ nixpkgs
, path
, ...
}:
let
  terraformApply = import (path "/makes/utils/terraform-apply") path nixpkgs;
in
terraformApply {
  name = "serves-secrets-apply";
  product = "serves";
  target = "serves/secrets/terraform";
}
