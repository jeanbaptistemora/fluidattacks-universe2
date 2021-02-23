{ servesPkgs
, path
, ...
}:
let
  terraformApply = import (path "/makes/utils/terraform-apply") path servesPkgs;
in
terraformApply {
  name = "serves-users-asserts-apply";
  product = "serves";
  target = "serves/users/asserts/terraform";
}
