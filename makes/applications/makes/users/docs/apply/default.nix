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
  target = "makes/makes/users/docs/infra";
  secretsPath = "makes/makes/secrets/prod.yaml";
}
