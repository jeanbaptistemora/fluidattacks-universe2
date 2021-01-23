{ meltsPkgs
, path
, ...
} @ attrs:
let
  config = import (path "/makes/products/melts/config") attrs.copy;
  makeDerivation = import (path "/makes/utils/make-derivation") path meltsPkgs;
in
makeDerivation {
  builder = path "/makes/products/melts/lint/builder.sh";
  envBashLibLintPython = import (path "/makes/utils/lint-python") path meltsPkgs;
  envSetupMeltsRuntime = config.setupMeltsRuntime;
  envSetupMeltsDevelopment = config.setupMeltsDevelopment;
  envSrcMeltsToolbox = path "/melts/toolbox";
  envSrcMeltsTest = path "/melts/tests";
  name = "melts-lint";
}
