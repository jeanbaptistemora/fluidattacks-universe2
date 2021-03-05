{ nixpkgs
, path
, ...
}:
let
  terraformApply = import (path "/makes/utils/terraform-apply") path nixpkgs;
in
terraformApply {
  name = "serves-users-sorts-apply";
  product = "serves";
  target = "serves/users/sorts/terraform";
}
