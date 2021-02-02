{ path
, integratesPkgsTerraform
, ...
} @ _:
let
  terraformTest = import (path "/makes/utils/terraform-test") path integratesPkgsTerraform;
in
terraformTest {
  name = "integrates-infra-cache-db-test";
  product = "integrates";
  target = "integrates/deploy/cache-db/terraform";
}
