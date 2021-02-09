{ servesPkgsTerraform
, path
, ...
} @ _:
let
  terraformApplyCloudflare = import (path "/makes/utils/terraform-apply-with-cloudflare") path servesPkgsTerraform;
in
terraformApplyCloudflare {
  name = "serves-users-airs-apply";
  product = "serves";
  target = "serves/users/airs/terraform";
  secrets_path = "serves/secrets/production.yaml";
}
