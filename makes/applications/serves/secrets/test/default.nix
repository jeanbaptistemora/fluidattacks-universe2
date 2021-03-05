{ nixpkgs
, path
, ...
}:
let
  terraformTest = import (path "/makes/utils/terraform-test") path nixpkgs;
in
terraformTest {
  name = "serves-secrets-test";
  product = "serves";
  target = "serves/secrets/terraform";
}
