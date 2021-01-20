{ forcesPkgs
, path
, ...
} @ attrs:
let
  config = import (path "/makes/forces/config") attrs.copy;
  makeEntrypoint = import (path "/makes/utils/make-entrypoint") path forcesPkgs;
in
makeEntrypoint {
  arguments = {
    envSetupForcesRuntime = config.setupForcesRuntime;
  };
  location = "/bin/forces";
  name = "forces-bin";
  template = path "/makes/forces/bin/entrypoint.sh";
}
