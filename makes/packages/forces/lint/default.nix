{ forcesPkgs
, packages
, path
, ...
} @ _:
let
  makeDerivation = import (path "/makes/utils/make-derivation") path forcesPkgs;
in
makeDerivation {
  builder = path "/makes/packages/forces/lint/builder.sh";
  envBashLibLintPython = import (path "/makes/utils/lint-python") path forcesPkgs;
  envSetupForcesRuntime = packages.forces.config-runtime;
  envSetupForcesDevelopment = packages.forces.config-development;
  envSrcForcesForces = path "/forces/forces";
  envSrcForcesTest = path "/forces/test";
  name = "forces-lint";
}
