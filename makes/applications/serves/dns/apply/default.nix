{ servesPkgsTerraform
, path
, ...
} @ _:
let
  terraformApplyCloudflare = import (path "/makes/utils/terraform-apply-with-cloudflare") path servesPkgsTerraform;
in
terraformApplyCloudflare {
  name = "serves-dns-apply";
  product = "serves";
  target = "serves/dns/terraform";
  secrets_path = "serves/secrets/production.yaml";
}
