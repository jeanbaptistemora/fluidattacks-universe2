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
    sources.packages."integrates/front/lint/eslint"
    sources.packages."integrates/front/lint/stylelint"
    sources.packages."integrates/front/lint/tslint"
  ];
  name = "integrates-front-lint";
}
