{ makeEntrypoint
, packages
, path
, ...
}:
makeEntrypoint {
  arguments = {
    envSetupForcesRuntime = packages.forces.config-runtime;
  };
  name = "forces";
  template = path "/makes/applications/forces/entrypoint.sh";
}
