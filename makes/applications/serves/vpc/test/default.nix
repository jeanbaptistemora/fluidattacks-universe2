{ servesPkgsTerraform
, path
, ...
} @ _:
let
  terraformTest = import (path "/makes/utils/terraform-test") path servesPkgsTerraform;
in
terraformTest {
  name = "serves-vpc-test";
  product = "serves";
  target = "serves/vpc/terraform";
  secretsPath = "serves/secrets/development.yaml";
}
