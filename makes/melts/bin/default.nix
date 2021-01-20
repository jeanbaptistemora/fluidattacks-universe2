{ meltsPkgs
, path
, ...
} @ attrs:
let
  config = import (path "/makes/melts/config") attrs.copy;
  makeEntrypoint = import (path "/makes/utils/make-entrypoint") path meltsPkgs;
in
makeEntrypoint {
  arguments = {
    envSetupMeltsRuntime = config.setupMeltsRuntime;
  };
  location = "/bin/melts";
  name = "melts-bin";
  template = path "/makes/melts/bin/entrypoint.sh";
}
