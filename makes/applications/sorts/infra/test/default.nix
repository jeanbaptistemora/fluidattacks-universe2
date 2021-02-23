{ path
, sortsPkgs
, ...
}:
let
  terraformTest = import (path "/makes/utils/terraform-test") path sortsPkgs;
in
terraformTest {
  name = "sorts-infra-test";
  product = "sorts";
  target = "sorts/infra";
}
