{ path
, integratesPkgsTerraform
, ...
} @ _:
let
  terraformTest = import (path "/makes/utils/terraform-apply") path integratesPkgsTerraform;
in
terraformTest {
  name = "integrates-infra-cache-db-apply";
  product = "integrates";
  target = "integrates/deploy/cache-db/terraform";
}
