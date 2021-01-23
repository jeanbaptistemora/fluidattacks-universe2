{ path
, sortsPkgs
, ...
} @ attrs:
let
  config = import (path "/makes/products/sorts/config") attrs.copy;
  makeEntrypoint = import (path "/makes/utils/make-entrypoint") path sortsPkgs;
in
makeEntrypoint {
  arguments = {
    envSetupSortsRuntime = config.setupSortsRuntime;
  };
  location = "/bin/sorts";
  name = "sorts-bin";
  template = path "/makes/products/sorts/bin/entrypoint.sh";
}
