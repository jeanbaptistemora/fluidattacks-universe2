{ forcesPkgs
, packages
, path
, ...
}:
let
  makeEntrypoint = import (path "/makes/utils/make-entrypoint") path forcesPkgs;
in
makeEntrypoint {
  arguments = {
    envSetupForcesRuntime = packages.forces.config-runtime;
  };
  name = "forces";
  template = path "/makes/applications/forces/entrypoint.sh";
}
