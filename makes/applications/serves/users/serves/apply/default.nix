{ servesPkgs
, path
, ...
} @ _:
let
  terraformApply = import (path "/makes/utils/terraform-apply") path servesPkgs;
in
terraformApply {
  name = "serves-users-serves-apply";
  product = "serves";
  target = "serves/users/serves/terraform";
}
