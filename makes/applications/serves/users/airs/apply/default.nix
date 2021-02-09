{ servesPkgsTerraform
, path
, ...
} @ _:
let
  terraformApply = import (path "/makes/utils/terraform-apply") path servesPkgsTerraform;
in
terraformApply {
  name = "serves-users-airs-apply";
  product = "serves";
  target = "serves/users/airs/terraform";
  secrets_path = "serves/secrets/production.yaml";
}
