{ servesPkgs
, path
, ...
} @ _:
let
  terraformApply = import (path "/makes/utils/terraform-apply") path servesPkgs;
in
terraformApply {
  name = "serves-dns-apply";
  product = "serves";
  target = "serves/dns/terraform";
  secretsPath = "serves/secrets/production.yaml";
}
