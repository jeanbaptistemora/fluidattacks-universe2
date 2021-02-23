{ meltsPkgs
, packages
, path
, ...
}:
let
  makeEntrypoint = import (path "/makes/utils/make-entrypoint") path meltsPkgs;
in
makeEntrypoint {
  arguments = {
    envSetupMeltsRuntime = packages.melts.config-runtime;
  };
  name = "melts";
  template = path "/makes/applications/melts/entrypoint.sh";
}
