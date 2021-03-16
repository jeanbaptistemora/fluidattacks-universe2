{ nixpkgs
, path
, ...
}:
let
  terraformApply = import (path "/makes/utils/terraform-apply") path nixpkgs;
in
terraformApply {
  name = "serves-users-melts-apply";
  product = "serves";
  target = "makes/applications/serves/users/melts/src/terraform";
}
