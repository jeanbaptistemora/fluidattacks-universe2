{ nixpkgs
, path
, ...
}:
let
  terraformTest = import (path "/makes/utils/terraform-test") path nixpkgs;
in
terraformTest {
  name = "makes-dns-test";
  product = "makes";
  target = "makes/applications/makes/dns/src/terraform";
  secretsPath = "makes/applications/serves/secrets/src/development.yaml";
}
