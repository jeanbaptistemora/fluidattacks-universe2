{ forcesPkgs
, ...
} @ attrs:
let
  config = import ../../../makes/forces/config attrs.copy;
  makeDerivation = import ../../../makes/utils/make-derivation forcesPkgs;
in
makeDerivation {
  builder = ./builder.sh;
  envBashLibLintPython = import ../../../makes/utils/bash-lib/lint-python forcesPkgs;
  envSetupForcesRuntime = config.setupForcesRuntime;
  envSetupForcesDevelopment = config.setupForcesDevelopment;
  envSrcForcesForces = ../../../forces/forces;
  envSrcForcesTest = ../../../forces/test;
  name = "forces-lint";
}
