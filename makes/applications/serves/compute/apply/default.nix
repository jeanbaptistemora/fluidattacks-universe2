{ nixpkgs
, path
, ...
}:
let
  terraformApply = import (path "/makes/utils/terraform-apply") path nixpkgs;
in
terraformApply {
  name = "serves-compute-apply";
  product = "serves";
  target = "makes/applications/serves/compute/src/terraform";
}
