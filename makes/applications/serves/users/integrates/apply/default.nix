{ servesPkgs
, path
, ...
}:
let
  terraformApply = import (path "/makes/utils/terraform-apply") path servesPkgs;
in
terraformApply {
  name = "serves-users-integrates-apply";
  product = "serves";
  target = "serves/users/integrates/terraform";
  secretsPath = "serves/secrets/production.yaml";
}
