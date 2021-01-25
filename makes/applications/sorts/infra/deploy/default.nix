{ path
, sortsPkgs
, ...
} @ _:
let
  terraformApply = import (path "/makes/utils/terraform-apply") path sortsPkgs;
in
terraformApply {
  name = "sorts-infra-deploy";
  product = "sorts";
  target = "sorts/infra";
}
