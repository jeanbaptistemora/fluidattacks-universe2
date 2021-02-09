{ servesPkgsTerraform
, path
, ...
} @ _:
let
  terraformTest = import (path "/makes/utils/terraform-test") path servesPkgsTerraform;
in
terraformTest {
  name = "serves-users-integrates-test";
  product = "serves";
  target = "serves/users/integrates/terraform";
  secrets_path = "serves/secrets/development.yaml";
}
