{ packages
, path
, sortsPkgs
, ...
} @ _:
let
  makeEntrypoint = import (path "/makes/utils/make-entrypoint") path sortsPkgs;
in
makeEntrypoint {
  arguments = {
    envSetupSortsRuntime = packages.sorts.config-runtime;
  };
  name = "sorts";
  template = path "/makes/applications/sorts/entrypoint.sh";
}
