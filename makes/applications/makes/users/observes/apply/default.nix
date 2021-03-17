{ nixpkgs
, path
, ...
}:
let
  terraformApply = import (path "/makes/utils/terraform-apply") path nixpkgs;
in
terraformApply {
  name = "makes-users-observes-apply";
  product = "makes";
  target = "makes/applications/makes/users/observes/src/terraform";
}
