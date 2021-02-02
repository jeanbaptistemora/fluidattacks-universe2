{ path
, integratesPkgsTerraform
, ...
} @ _:
let
  terraformTest = import (path "/makes/utils/terraform-test") path integratesPkgsTerraform;
in
terraformTest {
  name = "integrates-infra-database-test";
  product = "integrates";
  target = "integrates/deploy/database/terraform";
}
