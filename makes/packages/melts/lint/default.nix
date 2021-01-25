{ meltsPkgs
, path
, ...
} @ attrs:
let
  makeDerivation = import (path "/makes/utils/make-derivation") path meltsPkgs;
in
makeDerivation {
  builder = path "/makes/packages/melts/lint/builder.sh";
  envBashLibLintPython = import (path "/makes/utils/lint-python") path meltsPkgs;
  envSetupMeltsDevelopment = import (path "/makes/packages/melts/config-development") attrs.copy;
  envSetupMeltsRuntime = import (path "/makes/packages/melts/config-runtime") attrs.copy;
  envSrcMeltsToolbox = path "/melts/toolbox";
  envSrcMeltsTest = path "/melts/tests";
  name = "melts-lint";
}
