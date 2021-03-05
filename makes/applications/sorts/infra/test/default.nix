{ path
, nixpkgs
, ...
}:
let
  terraformTest = import (path "/makes/utils/terraform-test") path nixpkgs;
in
terraformTest {
  name = "sorts-infra-test";
  product = "sorts";
  target = "sorts/infra";
}
