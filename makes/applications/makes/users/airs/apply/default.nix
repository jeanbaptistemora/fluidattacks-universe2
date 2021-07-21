{ nixpkgs
, path
, ...
}:
let
  terraformApply = import (path "/makes/utils/terraform-apply") path nixpkgs;
in
terraformApply {
  name = "makes-users-airs-apply";
  product = "makes";
  target = "makes/applications/makes/users/airs/src/terraform";
  secretsPath = "makes/makes/secrets/prod.yaml";
}
