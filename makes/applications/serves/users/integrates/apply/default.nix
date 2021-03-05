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
  secretsPath = "serves/secrets/production.yaml";
}
