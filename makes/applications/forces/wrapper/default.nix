{ forcesPkgs
, packages
, path
, ...
} @ _:
let
  makeEntrypoint = import (path "/makes/utils/make-entrypoint") path forcesPkgs;
in
makeEntrypoint {
  arguments = {
    envSetupForcesWrapper = packages.forces.config-wrapper;
  };
  name = "forces-wrapper";
  template = path "/makes/applications/forces/wrapper/entrypoint.sh";
}
