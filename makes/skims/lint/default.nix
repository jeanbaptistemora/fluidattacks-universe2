{ path
, skimsPkgs
, ...
} @ attrs:
let
  config = import (path "/makes/skims/config") attrs.copy;
  makeDerivation = import (path "/makes/utils/make-derivation") skimsPkgs;
in
makeDerivation {
  builder = ./builder.sh;
  envBashLibLintPython = import (path "/makes/utils/bash-lib/lint-python") skimsPkgs;
  envImportLinterConfig = (path "/skims/setup.imports.cfg");
  envSetupSkimsDevelopment = config.setupSkimsDevelopment;
  envSetupSkimsRuntime = config.setupSkimsRuntime;
  envSrcSkimsSkims = (path "/skims/skims");
  envSrcSkimsTest = (path "/skims/test");
  name = "skims-lint";
}
