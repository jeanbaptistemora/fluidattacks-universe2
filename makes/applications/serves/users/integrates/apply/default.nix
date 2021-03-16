{ nixpkgs
, path
, ...
}:
let
  terraformApply = import (path "/makes/utils/terraform-apply") path nixpkgs;
in
terraformApply {
  name = "serves-users-integrates-apply";
  product = "serves";
  target = "makes/applications/serves/users/integrates/src/terraform";
  secretsPath = "makes/applications/serves/secrets/src/production.yaml";
}
