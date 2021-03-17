{ nixpkgs
, path
, ...
}:
let
  terraformTest = import (path "/makes/utils/terraform-test") path nixpkgs;
in
terraformTest {
  name = "makes-ci-test";
  product = "makes";
  target = "makes/applications/makes/ci/src/terraform";
}
