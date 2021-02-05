{ meltsPkgs
, path
, ...
} @ attrs:
let
  makeEntrypoint = import (path "/makes/utils/make-entrypoint") path meltsPkgs;
in
makeEntrypoint {
  arguments = {
    envSetupMeltsRuntime = import (path "/makes/packages/melts/config-runtime") attrs.copy;
  };
  name = "melts";
  template = path "/makes/applications/melts/entrypoint.sh";
}
