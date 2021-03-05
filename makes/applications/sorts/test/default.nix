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
    envSetupSortsDevelopment = packages.sorts.config-development;
    envSetupSortsRuntime = packages.sorts.config-runtime;
    envSrcSortsSorts = path "/sorts/sorts";
  };
  name = "sorts-test";
  template = path "/makes/applications/sorts/test/entrypoint.sh";
}
