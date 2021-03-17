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
  target = "makes/applications/serves/users/airs/src/terraform";
  secretsPath = "makes/applications/makes/secrets/src/development.yaml";
}
