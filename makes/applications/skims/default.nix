{ packages
, path
, skimsPkgs
, ...
}:
let
  makeEntrypoint = import (path "/makes/utils/make-entrypoint") path skimsPkgs;
in
makeEntrypoint {
  arguments = {
    envSetupSkimsRuntime = packages.skims.config-runtime;
  };
  name = "skims";
  template = path "/makes/applications/skims/entrypoint.sh";
}
