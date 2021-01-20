{ observesPkgs
, ...
} @ attrs:
let
  config = import ../../../makes/observes/config attrs.copy;
  makeDerivation = import ../../../makes/utils/make-derivation observesPkgs;
in
makeDerivation {
  builder = ./builder.sh;
  envBashLibLintPython = import ../../../makes/utils/bash-lib/lint-python observesPkgs;
  envSetupObservesTargetRedshift = config.setupObservesTargetRedshiftRuntime;
  envSrcObservesTargetRedshift = ../../../observes/singer/target_redshift;
  name = "observes-target-redshift-lint";
}
