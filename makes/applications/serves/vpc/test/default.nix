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
  target = "serves/vpc/terraform";
  secretsPath = "serves/secrets/development.yaml";
}
