{ nixpkgs
, path
, ...
}:
let
  terraformApply = import (path "/makes/utils/terraform-apply") path nixpkgs;
in
terraformApply {
  name = "serves-vpc-apply";
  product = "serves";
  target = "serves/vpc/terraform";
  secretsPath = "serves/secrets/production.yaml";
}
