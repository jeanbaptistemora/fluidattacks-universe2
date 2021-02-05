{ forcesPkgs
, path
, ...
} @ attrs:
let
  makeEntrypoint = import (path "/makes/utils/make-entrypoint") path forcesPkgs;
in
makeEntrypoint {
  arguments = {
    envSetupForcesRuntime = import (path "/makes/packages/forces/config-runtime") attrs.copy;
  };
  name = "forces";
  template = path "/makes/applications/forces/entrypoint.sh";
}
