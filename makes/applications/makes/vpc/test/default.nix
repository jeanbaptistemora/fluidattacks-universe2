{ nixpkgs
, path
, ...
}:
let
  terraformTest = import (path "/makes/utils/terraform-test") path nixpkgs;
in
terraformTest {
  name = "makes-vpc-test";
  product = "makes";
  target = "makes/applications/makes/vpc/src/terraform";
  secretsPath = "makes/applications/makes/secrets/src/development.yaml";
}
