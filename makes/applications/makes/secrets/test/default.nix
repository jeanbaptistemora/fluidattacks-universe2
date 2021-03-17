{ nixpkgs
, path
, ...
}:
let
  terraformTest = import (path "/makes/utils/terraform-test") path nixpkgs;
in
terraformTest {
  name = "makes-secrets-test";
  product = "makes";
  target = "makes/applications/makes/secrets/src/terraform";
}
