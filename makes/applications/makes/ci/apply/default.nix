{ nixpkgs
, path
, ...
}:
let
  terraformApply = import (path "/makes/utils/terraform-apply") path nixpkgs;
in
terraformApply {
  name = "makes-ci-apply";
  product = "makes";
  target = "makes/applications/makes/ci/src/terraform";
}
