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
  target = "makes/makes/users/docs/infra";
  secretsPath = "makes/makes/secrets/dev.yaml";
}
