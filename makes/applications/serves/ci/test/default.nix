{ nixpkgs
, path
, ...
}:
let
  terraformTest = import (path "/makes/utils/terraform-test") path nixpkgs;
in
terraformTest {
  name = "serves-ci-test";
  product = "serves";
  target = "makes/applications/serves/ci/src/terraform";
}
