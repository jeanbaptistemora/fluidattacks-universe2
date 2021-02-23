{ servesPkgs
, path
, ...
}:
let
  terraformApply = import (path "/makes/utils/terraform-apply") path servesPkgs;
in
terraformApply {
  name = "serves-users-services-apply";
  product = "serves";
  target = "serves/users/services/terraform";
}
