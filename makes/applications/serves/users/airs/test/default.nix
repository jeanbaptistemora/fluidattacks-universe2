{ servesPkgsTerraform
, path
, ...
} @ _:
let
  terraformTestCloudflare = import (path "/makes/utils/terraform-test-with-cloudflare") path servesPkgsTerraform;
in
terraformTestCloudflare {
  name = "serves-users-airs-test";
  product = "serves";
  target = "serves/users/airs/terraform";
  secrets_path = "serves/secrets/development.yaml";
}
