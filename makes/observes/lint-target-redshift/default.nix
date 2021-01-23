{ observesPkgs
, path
, ...
} @ attrs:
let
  config = import (path "/makes/observes/config") attrs.copy;
  makeDerivation = import (path "/makes/utils/make-derivation") path observesPkgs;
in
makeDerivation {
  builder = path "/makes/observes/lint-target-redshift/builder.sh";
  envBashLibLintPython = import (path "/makes/utils/lint-python") path observesPkgs;
  envSetupObservesTargetRedshift = config.setupObservesTargetRedshiftRuntime;
  envSrcObservesTargetRedshift = path "/observes/singer/target_redshift";
  name = "observes-target-redshift-lint";
}
