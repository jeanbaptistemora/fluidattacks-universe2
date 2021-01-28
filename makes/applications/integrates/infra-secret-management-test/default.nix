{ path
, integratesPkgsTerraform
, ...
} @ _:
let
  terraformTest = import (path "/makes/utils/terraform-test") path integratesPkgsTerraform;
in
terraformTest {
  name = "integrates-infra-secret-management-test";
  product = "integrates";
  target = "integrates/deploy/secret-management/terraform";
}
