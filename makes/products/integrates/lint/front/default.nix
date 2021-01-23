{ integratesPkgs
, path
, ...
} @ _:
let
  makeDerivation = import (path "/makes/utils/make-derivation") path integratesPkgs;
in
makeDerivation {
  builder = path "/makes/products/integrates/lint/front/builder.sh";
  envSrcIntegratesFront = path "/integrates/front";
  name = "integrates-lint-front";
}
