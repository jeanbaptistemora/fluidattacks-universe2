{ servesPkgsTerraform
, path
, ...
} @ _:
let
  terraformTest = import (path "/makes/utils/terraform-test") path servesPkgsTerraform;
in
terraformTest {
  name = "serves-users-airs-test";
  product = "serves";
  target = "serves/users/airs/terraform";
  secrets_path = "serves/secrets/development.yaml";
}
