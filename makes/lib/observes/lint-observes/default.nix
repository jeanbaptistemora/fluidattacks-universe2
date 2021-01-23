{ buildInputs
, observesPkgs
, packageSrcPath
, path
}:
let
  makeDerivation = import (path "/makes/utils/make-derivation") path observesPkgs;
  lintPython = import (path "/makes/utils/lint-python") path observesPkgs;
in
makeDerivation {
  builder = path "/makes/lib/observes/lint-observes/builder.sh";
  buildInputs = buildInputs ++ [
    lintPython
  ];
  envSrc = packageSrcPath;
  name = "observes-lint";
}
