{ nixpkgs
, path
, ...
}:
let
  terraformTest = import (path "/makes/utils/terraform-test") path nixpkgs;
in
terraformTest {
  name = "serves-vpc-test";
  product = "serves";
  target = "makes/applications/serves/vpc/src/terraform";
  secretsPath = "makes/applications/serves/secrets/src/development.yaml";
}
