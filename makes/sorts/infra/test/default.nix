{ path
, sortsPkgs
, ...
} @ _:
let
  terraformTest = import (path "/makes/utils/bash-lib/terraform-test") path sortsPkgs;
in
terraformTest {
  name = "sorts-infra-test";
  product = "sorts";
  target = "sorts/infra";
}
