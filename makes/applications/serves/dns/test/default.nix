{ servesPkgsTerraform
, path
, ...
} @ _:
let
  terraformTestCloudflare = import (path "/makes/utils/terraform-test-with-cloudflare") path servesPkgsTerraform;
in
terraformTestCloudflare {
  name = "serves-dns-test";
  product = "serves";
  target = "serves/dns/terraform";
  secrets_path = "serves/secrets/development.yaml";
}
