{ path
, nixpkgs
, ...
}:
let
  terraformApply = import (path "/makes/utils/terraform-apply") path nixpkgs;
in
terraformApply {
  name = "sorts-infra-deploy";
  product = "sorts";
  target = "sorts/infra";
}
