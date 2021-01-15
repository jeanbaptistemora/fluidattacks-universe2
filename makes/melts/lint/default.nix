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
  envSrcMelts = ../../../melts/toolbox;
  name = "melts-lint";
}
