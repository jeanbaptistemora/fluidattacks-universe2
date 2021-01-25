{ forcesPkgs
, path
, ...
} @ attrs:
let
  makeDerivation = import (path "/makes/utils/make-derivation") path forcesPkgs;
in
makeDerivation {
  builder = path "/makes/packages/forces/lint/builder.sh";
  envBashLibLintPython = import (path "/makes/utils/lint-python") path forcesPkgs;
  envSetupForcesRuntime = import (path "/makes/packages/forces/config-runtime") attrs.copy;
  envSetupForcesDevelopment = import (path "/makes/packages/forces/config-development") attrs.copy;
  envSrcForcesForces = path "/forces/forces";
  envSrcForcesTest = path "/forces/test";
  name = "forces-lint";
}
