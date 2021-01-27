{ integratesPkgs
, path
, sources
, ...
} @ _:
let
  makeDerivation = import (path "/makes/utils/make-derivation") path integratesPkgs;
in
makeDerivation {
  builder = "success";
  envBuilt = [
    sources.packages."integrates/lint/front/eslint"
    sources.packages."integrates/lint/front/tslint"
  ];
  name = "integrates-lint-front";
}
