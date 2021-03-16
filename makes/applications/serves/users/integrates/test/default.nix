{ nixpkgs
, path
, ...
}:
let
  terraformTest = import (path "/makes/utils/terraform-test") path nixpkgs;
in
terraformTest {
  name = "serves-users-integrates-test";
  product = "serves";
  target = "serves/users/integrates/terraform";
  secretsPath = "makes/applications/serves/secrets/src/development.yaml";
}
