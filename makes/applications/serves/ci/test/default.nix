{ servesPkgs
, path
, ...
}:
let
  terraformTest = import (path "/makes/utils/terraform-test") path servesPkgs;
in
terraformTest {
  name = "serves-ci-test";
  product = "serves";
  target = "serves/ci/terraform";
}
