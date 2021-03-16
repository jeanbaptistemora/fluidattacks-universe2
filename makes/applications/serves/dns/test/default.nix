{ nixpkgs
, path
, ...
}:
let
  terraformTest = import (path "/makes/utils/terraform-test") path nixpkgs;
in
terraformTest {
  name = "serves-dns-test";
  product = "serves";
  target = "makes/applications/serves/dns/src/terraform";
  secretsPath = "makes/applications/serves/secrets/src/development.yaml";
}
