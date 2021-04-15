{ nixpkgs
, path
, ...
}:
let
  terraformTest = import (path "/makes/utils/terraform-test") path nixpkgs;
in
terraformTest {
  name = "makes-users-docs-test";
  product = "makes";
  target = "makes/applications/makes/users/docs/src/terraform";
  secretsPath = "makes/applications/makes/secrets/src/development.yaml";
}
