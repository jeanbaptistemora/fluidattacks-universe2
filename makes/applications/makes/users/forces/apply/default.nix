{ nixpkgs
, path
, ...
}:
let
  terraformApply = import (path "/makes/utils/terraform-apply") path nixpkgs;
in
terraformApply {
  name = "makes-users-forces-apply";
  product = "makes";
  target = "makes/applications/makes/users/forces/src/terraform";
}
