{ nixpkgs
, path
, ...
}:
let
  terraformApply = import (path "/makes/utils/terraform-apply") path nixpkgs;
in
terraformApply {
  name = "makes-users-integrates-apply";
  product = "makes";
  target = "makes/applications/makes/users/integrates/src/terraform";
  secretsPath = "makes/applications/makes/secrets/src/production.yaml";
}
