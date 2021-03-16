{ nixpkgs
, path
, ...
}:
let
  terraformTest = import (path "/makes/utils/terraform-test") path nixpkgs;
in
terraformTest {
  name = "serves-users-airs-test";
  product = "serves";
  target = "serves/users/airs/terraform";
  secretsPath = "makes/applications/serves/secrets/src/development.yaml";
}
