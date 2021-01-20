{ path
, skimsPkgs
, ...
} @ attrs:
let
  config = import (path "/makes/skims/config") attrs.copy;
  makeDerivation = import (path "/makes/utils/make-derivation") path skimsPkgs;
in
makeDerivation {
  builder = path "/makes/skims/lint/builder.sh";
  envBashLibLintPython = import (path "/makes/utils/bash-lib/lint-python") path skimsPkgs;
  envImportLinterConfig = path "/skims/setup.imports.cfg";
  envSetupSkimsDevelopment = config.setupSkimsDevelopment;
  envSetupSkimsRuntime = config.setupSkimsRuntime;
  envSrcSkimsSkims = path "/skims/skims";
  envSrcSkimsTest = path "/skims/test";
  name = "skims-lint";
}
