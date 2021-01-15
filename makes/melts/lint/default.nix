{ meltsPkgs
, ...
} @ attrs:
let
  config = import ../../../makes/melts/config attrs.copy;
  makeDerivation = import ../../../makes/utils/make-derivation meltsPkgs;
in
makeDerivation {
  builder = ./builder.sh;
  envBashLibLintPython = import ../../../makes/utils/bash-lib/lint-python meltsPkgs;
  envSetupMeltsRuntime = config.setupMeltsRuntime;
  envSetupMeltsDevelopment = config.setupMeltsDevelopment;
  envSrcMeltsToolbox = ../../../melts/toolbox;
  envSrcMeltsTest = ../../../melts/tests;
  name = "melts-lint";
}
