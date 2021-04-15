{ nixpkgs
, path
, ...
}:
let
  terraformApply = import (path "/makes/utils/terraform-apply") path nixpkgs;
in
terraformApply {
  name = "makes-users-docs-apply";
  product = "makes";
  target = "makes/applications/makes/users/docs/src/terraform";
  secretsPath = "makes/applications/makes/secrets/src/production.yaml";
}
