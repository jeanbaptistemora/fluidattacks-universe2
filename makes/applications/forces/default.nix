{ makeEntrypoint
, packages
, path
, ...
}:
makeEntrypoint {
  name = "forces";
  searchPaths = {
    envSources = [ packages.forces.config-runtime ];
  };
  template = path "/makes/applications/forces/entrypoint.sh";
}
