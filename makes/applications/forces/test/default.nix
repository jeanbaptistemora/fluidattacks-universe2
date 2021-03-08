{ makeEntrypoint
, packages
, path
, ...
}:
makeEntrypoint {
  name = "forces-test";
  searchPaths = {
    envSources = [
      packages.forces.config-development
      packages.forces.config-runtime
    ];
  };
  template = path "/makes/applications/forces/test/entrypoint.sh";
}
