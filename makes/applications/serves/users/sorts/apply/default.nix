{ servesPkgs
, path
, ...
} @ _:
let
  terraformApply = import (path "/makes/utils/terraform-apply") path servesPkgs;
in
terraformApply {
  name = "serves-users-sorts-apply";
  product = "serves";
  target = "serves/users/sorts/terraform";
}
