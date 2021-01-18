{ sortsPkgs
, ...
} @ _:
let
  terraformTest = import ../../../../makes/utils/bash-lib/terraform-test sortsPkgs;
in
terraformTest {
  name = "sorts-infra-test";
  path = "sorts/infra";
  product = "sorts";
}
