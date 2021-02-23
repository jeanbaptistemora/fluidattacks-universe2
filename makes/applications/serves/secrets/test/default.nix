{ servesPkgs
, path
, ...
}:
let
  terraformTest = import (path "/makes/utils/terraform-test") path servesPkgs;
in
terraformTest {
  name = "serves-secrets-test";
  product = "serves";
  target = "serves/secrets/terraform";
}
