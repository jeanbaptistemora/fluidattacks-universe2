{ forcesPkgs
, path
, ...
} @ attrs:
let
  config = import (path "/makes/products/forces/config") attrs.copy;
  makeDerivation = import (path "/makes/utils/make-derivation") path forcesPkgs;
in
makeDerivation {
  builder = path "/makes/products/forces/lint/builder.sh";
  envBashLibLintPython = import (path "/makes/utils/lint-python") path forcesPkgs;
  envSetupForcesRuntime = config.setupForcesRuntime;
  envSetupForcesDevelopment = config.setupForcesDevelopment;
  envSrcForcesForces = path "/forces/forces";
  envSrcForcesTest = path "/forces/test";
  name = "forces-lint";
}
