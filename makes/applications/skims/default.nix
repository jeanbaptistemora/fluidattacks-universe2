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
    envSetupSkimsRuntime = packages.skims.config-runtime;
  };
  name = "skims";
  template = path "/makes/applications/skims/entrypoint.sh";
}
