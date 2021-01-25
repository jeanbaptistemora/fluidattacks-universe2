{ path
, sortsPkgs
, ...
} @ attrs:
let
  makeEntrypoint = import (path "/makes/utils/make-entrypoint") path sortsPkgs;
in
makeEntrypoint {
  arguments = {
    envSetupSortsDevelopment = import (path "/makes/packages/sorts/config-development") attrs.copy;
    envSetupSortsRuntime = import (path "/makes/packages/sorts/config-runtime") attrs.copy;
    envSrcSortsSorts = path "/sorts/sorts";
  };
  name = "sorts-test";
  template = path "/makes/applications/sorts/test/entrypoint.sh";
}
