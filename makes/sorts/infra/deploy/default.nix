{ sortsPkgs
, ...
} @ _:
let
  terraformApply = import ../../../../makes/utils/bash-lib/terraform-apply sortsPkgs;
in
terraformApply {
  name = "sorts-infra-deploy";
  path = "sorts/infra";
  product = "sorts";
}
