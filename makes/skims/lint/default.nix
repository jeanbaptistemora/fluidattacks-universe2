{ skimsPkgs
, ...
} @ attrs:
let
  config = import ../../../makes/skims/config attrs.copy;
  makeDerivation = import ../../../makes/utils/make-derivation skimsPkgs;
in
makeDerivation {
  builder = ./builder.sh;
  envBashLibLintPython = import ../../../makes/utils/bash-lib/lint-python skimsPkgs;
  envImportLinterConfig = ../../../skims/setup.imports.cfg;
  envSetupSkimsDevelopment = config.setupSkimsDevelopment;
  envSetupSkimsRuntime = config.setupSkimsRuntime;
  envSrcSkimsSkims = ../../../skims/skims;
  envSrcSkimsTest = ../../../skims/test;
  name = "skims-lint";
}
