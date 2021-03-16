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
  target = "serves/users/airs/terraform";
  secretsPath = "makes/applications/serves/secrets/src/production.yaml";
}
