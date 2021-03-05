{ packages
, path
, nixpkgs
, ...
}:
let
  makeEntrypoint = import (path "/makes/utils/make-entrypoint") path nixpkgs;
in
makeEntrypoint {
  arguments = {
    envSetupSortsRuntime = packages.sorts.config-runtime;
  };
  name = "sorts";
  template = path "/makes/applications/sorts/entrypoint.sh";
}
