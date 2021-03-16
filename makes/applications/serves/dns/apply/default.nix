{ nixpkgs
, path
, ...
}:
let
  terraformApply = import (path "/makes/utils/terraform-apply") path nixpkgs;
in
terraformApply {
  name = "serves-dns-apply";
  product = "serves";
  target = "makes/applications/serves/dns/src/terraform";
  secretsPath = "serves/secrets/production.yaml";
}
