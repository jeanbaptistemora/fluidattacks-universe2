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
    envSetupSortsDevelopment = config.setupSortsDevelopment;
    envSetupSortsRuntime = config.setupSortsRuntime;
    envSrcSortsSorts = path "/sorts/sorts";
  };
  location = "/bin/sorts-test";
  name = "sorts-test";
  template = path "/makes/products/sorts/test/entrypoint.sh";
}
