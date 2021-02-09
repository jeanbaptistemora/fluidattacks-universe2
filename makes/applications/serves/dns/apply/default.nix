{ servesPkgsTerraform
, path
, ...
} @ _:
let
  terraformApply = import (path "/makes/utils/terraform-apply") path servesPkgsTerraform;
in
terraformApply {
  name = "serves-dns-apply";
  product = "serves";
  target = "serves/dns/terraform";
  secrets_path = "serves/secrets/production.yaml";
}
