{ meltsPkgs
, path
, ...
} @ attrs:
let
  config = import (path "/makes/products/melts/config") attrs.copy;
  makeEntrypoint = import (path "/makes/utils/make-entrypoint") path meltsPkgs;
in
makeEntrypoint {
  arguments = {
    envSetupMeltsRuntime = config.setupMeltsRuntime;
  };
  location = "/bin/melts";
  name = "melts-bin";
  template = path "/makes/products/melts/bin/entrypoint.sh";
}
