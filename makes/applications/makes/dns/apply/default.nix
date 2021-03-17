{ nixpkgs
, path
, ...
}:
let
  terraformApply = import (path "/makes/utils/terraform-apply") path nixpkgs;
in
terraformApply {
  name = "makes-dns-apply";
  product = "makes";
  target = "makes/applications/makes/dns/src/terraform";
  secretsPath = "makes/applications/makes/secrets/src/production.yaml";
}
