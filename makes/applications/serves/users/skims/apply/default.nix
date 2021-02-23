{ servesPkgs
, path
, ...
}:
let
  terraformApply = import (path "/makes/utils/terraform-apply") path servesPkgs;
in
terraformApply {
  name = "serves-users-skims-apply";
  product = "serves";
  target = "serves/users/skims/terraform";
}
