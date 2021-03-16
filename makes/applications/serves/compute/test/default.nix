{ nixpkgs
, path
, ...
}:
let
  terraformTest = import (path "/makes/utils/terraform-test") path nixpkgs;
in
terraformTest {
  name = "serves-compute-test";
  product = "serves";
  target = "makes/applications/serves/compute/src/terraform";
}
