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
    envSetupForcesDevelopment = import (path "/makes/packages/forces/config-development") attrs.copy;
  };
  name = "forces-test";
  template = path "/makes/applications/forces/test/entrypoint.sh";
}
