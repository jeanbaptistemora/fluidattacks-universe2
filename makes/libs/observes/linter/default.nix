{ nixPkgs
, observesPackage
, path
}:
let
  makeDerivation = import (path "/makes/utils/make-derivation") path nixPkgs;
  lintPython = import (path "/makes/utils/lint-python") path nixPkgs;
in
makeDerivation {
  builder = path "/makes/libs/observes/linter/builder.sh";
  buildInputs = observesPackage.buildInputs ++ [
    lintPython
  ];
  envSrc = observesPackage.packagePath;
  name = "observes-linter";
}
