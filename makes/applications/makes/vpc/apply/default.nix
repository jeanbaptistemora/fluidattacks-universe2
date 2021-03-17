{ nixpkgs
, path
, ...
}:
let
  terraformApply = import (path "/makes/utils/terraform-apply") path nixpkgs;
in
terraformApply {
  name = "makes-vpc-apply";
  product = "makes";
  target = "makes/applications/makes/vpc/src/terraform";
  secretsPath = "makes/applications/makes/secrets/src/production.yaml";
}
