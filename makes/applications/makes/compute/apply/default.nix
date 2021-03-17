{ nixpkgs
, path
, ...
}:
let
  terraformApply = import (path "/makes/utils/terraform-apply") path nixpkgs;
in
terraformApply {
  name = "makes-compute-apply";
  product = "makes";
  target = "makes/applications/makes/compute/src/terraform";
}
