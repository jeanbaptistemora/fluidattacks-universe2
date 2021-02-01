{ forcesPkgs
, path
, ...
} @ attrs:
let
  makeEntrypoint = import (path "/makes/utils/make-entrypoint") path forcesPkgs;
in
makeEntrypoint {
  arguments = {
    envSetupForcesWrapper = import (path "/makes/packages/forces/config-wrapper") attrs.copy;
  };
  name = "forces-wrapper";
  template = path "/makes/applications/forces/wrapper/entrypoint.sh";
}
