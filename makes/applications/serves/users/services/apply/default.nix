{ nixpkgs
, path
, ...
}:
let
  terraformApply = import (path "/makes/utils/terraform-apply") path nixpkgs;
in
terraformApply {
  name = "serves-users-services-apply";
  product = "serves";
  target = "serves/users/services/terraform";
}
