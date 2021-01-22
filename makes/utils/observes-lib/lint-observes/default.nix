{ buildInputs
, observesPkgs
, packageSrcPath
, path
}:
let
  makeDerivation = import (path "/makes/utils/make-derivation") path observesPkgs;
  lintPython = import (path "/makes/utils/bash-lib/lint-python") path observesPkgs;
in
makeDerivation {
  builder = path "/makes/utils/observes-lib/lint-observes/builder.sh";
  buildInputs = buildInputs ++ [
    lintPython
  ];
  envSrc = packageSrcPath;
  name = "observes-lint";
}
