{ servesPkgs
, path
, ...
} @ _:
let
  terraformTest = import (path "/makes/utils/terraform-test") path servesPkgs;
in
terraformTest {
  name = "serves-users-integrates-test";
  product = "serves";
  target = "serves/users/integrates/terraform";
  secretsPath = "serves/secrets/development.yaml";
}
