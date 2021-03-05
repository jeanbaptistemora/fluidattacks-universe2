{ nixpkgs
, path
, ...
}:
let
  terraformApply = import (path "/makes/utils/terraform-apply") path nixpkgs;
in
terraformApply {
  name = "serves-users-skims-apply";
  product = "serves";
  target = "serves/users/skims/terraform";
}
