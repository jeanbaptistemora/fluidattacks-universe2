{ nixpkgs
, packages
, path
, ...
}:
let
  makeDerivation = import (path "/makes/utils/make-derivation") path nixpkgs;
in
makeDerivation {
  arguments = {
    envBashLibLintPython = import (path "/makes/utils/lint-python") path nixpkgs;
    envSetupForcesRuntime = packages.forces.config-runtime;
    envSetupForcesDevelopment = packages.forces.config-development;
    envSrcForcesForces = path "/forces/forces";
    envSrcForcesTest = path "/forces/test";
  };
  builder = path "/makes/packages/forces/lint/builder.sh";
  name = "forces-lint";
}
