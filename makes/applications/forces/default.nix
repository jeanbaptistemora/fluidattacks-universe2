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
  };
  name = "forces";
  template = path "/makes/applications/forces/entrypoint.sh";
}
