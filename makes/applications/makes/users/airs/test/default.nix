{ nixpkgs
, path
, ...
}:
let
  terraformTest = import (path "/makes/utils/terraform-test") path nixpkgs;
in
terraformTest {
  name = "makes-users-airs-test";
  product = "makes";
  target = "makes/applications/makes/users/airs/src/terraform";
  secretsPath = "makes/applications/makes/secrets/src/development.yaml";
}
