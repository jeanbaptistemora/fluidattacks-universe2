{ nixpkgs
, path
, ...
}:
let
  terraformApply = import (path "/makes/utils/terraform-apply") path nixpkgs;
in
terraformApply {
  name = "serves-ci-apply";
  product = "serves";
  target = "serves/ci/terraform";
}
