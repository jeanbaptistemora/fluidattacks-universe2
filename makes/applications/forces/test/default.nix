{ nixpkgs
, packages
, path
, ...
}:
let
  makeEntrypoint = import (path "/makes/utils/make-entrypoint") path nixpkgs;
in
makeEntrypoint {
  arguments = {
    envSetupForcesRuntime = packages.forces.config-runtime;
    envSetupForcesDevelopment = packages.forces.config-development;
  };
  name = "forces-test";
  template = path "/makes/applications/forces/test/entrypoint.sh";
}
