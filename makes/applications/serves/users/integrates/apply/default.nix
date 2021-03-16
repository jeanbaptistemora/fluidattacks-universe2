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
  target = "serves/users/integrates/terraform";
  secretsPath = "makes/applications/serves/secrets/src/production.yaml";
}
