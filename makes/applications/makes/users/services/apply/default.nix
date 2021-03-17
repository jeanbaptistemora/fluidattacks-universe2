{ nixpkgs
, path
, ...
}:
let
  terraformApply = import (path "/makes/utils/terraform-apply") path nixpkgs;
in
terraformApply {
  name = "makes-users-services-apply";
  product = "makes";
  target = "makes/applications/makes/users/services/src/terraform";
}
