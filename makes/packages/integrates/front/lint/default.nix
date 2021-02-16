{ integratesPkgs
, packages
, path
, ...
} @ _:
let
  makeDerivation = import (path "/makes/utils/make-derivation") path integratesPkgs;
in
makeDerivation {
  builder = "success";
  envBuilt = [
    packages.integrates.front.lint.eslint
    packages.integrates.front.lint.stylelint
    packages.integrates.front.lint.tslint
  ];
  name = "integrates-front-lint";
}
