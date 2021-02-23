{ servesPkgs
, path
, ...
}:
let
  terraformApply = import (path "/makes/utils/terraform-apply") path servesPkgs;
in
terraformApply {
  name = "serves-users-airs-apply";
  product = "serves";
  target = "serves/users/airs/terraform";
  secretsPath = "serves/secrets/production.yaml";
}
