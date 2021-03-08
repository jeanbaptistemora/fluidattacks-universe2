{ makeDerivation
, packages
, path
, ...
}:
makeDerivation {
  arguments = {
    envSrcForcesForces = path "/forces/forces";
    envSrcForcesTest = path "/forces/test";
  };
  builder = path "/makes/packages/forces/lint/builder.sh";
  name = "forces-lint";
  searchPaths = {
    envSources = [
      packages.forces.config-development
      packages.forces.config-runtime
    ];
    envUtils = [ "/makes/utils/lint-python" ];
  };
}
