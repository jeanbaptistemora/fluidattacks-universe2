{ path
, sortsPkgs
, ...
} @ attrs:
let
  makeEntrypoint = import (path "/makes/utils/make-entrypoint") path sortsPkgs;
in
makeEntrypoint {
  arguments = {
    envSetupSortsRuntime = import (path "/makes/packages/sorts/config-runtime") attrs.copy;
  };
  name = "sorts";
  template = path "/makes/applications/sorts/entrypoint.sh";
}
