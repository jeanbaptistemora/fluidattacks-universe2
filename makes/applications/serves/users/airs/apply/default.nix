{ nixpkgs
, path
, ...
}:
let
  terraformApply = import (path "/makes/utils/terraform-apply") path nixpkgs;
in
terraformApply {
  name = "serves-users-airs-apply";
  product = "serves";
  target = "makes/applications/serves/users/airs/src/terraform";
  secretsPath = "makes/applications/makes/secrets/src/production.yaml";
}
