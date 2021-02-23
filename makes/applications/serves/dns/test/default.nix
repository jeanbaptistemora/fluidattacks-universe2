{ servesPkgs
, path
, ...
}:
let
  terraformTest = import (path "/makes/utils/terraform-test") path servesPkgs;
in
terraformTest {
  name = "serves-dns-test";
  product = "serves";
  target = "serves/dns/terraform";
  secretsPath = "serves/secrets/development.yaml";
}
