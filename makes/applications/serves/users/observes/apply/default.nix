{ servesPkgs
, path
, ...
} @ _:
let
  terraformApply = import (path "/makes/utils/terraform-apply") path servesPkgs;
in
terraformApply {
  name = "serves-users-observes-apply";
  product = "serves";
  target = "serves/users/observes/terraform";
}
