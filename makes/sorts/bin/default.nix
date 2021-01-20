{ path
, sortsPkgs
, ...
} @ attrs:
let
  config = import (path "/makes/sorts/config") attrs.copy;
  makeEntrypoint = import (path "/makes/utils/make-entrypoint") path sortsPkgs;
in
makeEntrypoint {
  arguments = {
    envSetupSortsRuntime = config.setupSortsRuntime;
  };
  location = "/bin/sorts";
  name = "sorts-bin";
  template = path "/makes/sorts/bin/entrypoint.sh";
}
