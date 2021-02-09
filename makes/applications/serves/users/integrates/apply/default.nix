{ servesPkgsTerraform
, path
, ...
} @ _:
let
  terraformApply = import (path "/makes/utils/terraform-apply") path servesPkgsTerraform;
in
terraformApply {
  name = "serves-users-integrates-apply";
  product = "serves";
  target = "serves/users/integrates/terraform";
  secrets_path = "serves/secrets/production.yaml";
}
