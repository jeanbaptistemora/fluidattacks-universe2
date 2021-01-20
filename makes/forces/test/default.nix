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
    envSetupForcesDevelopment = config.setupForcesDevelopment;
  };
  location = "/bin/forces-test";
  name = "forces-test";
  template = path "/makes/forces/test/entrypoint.sh";
}
