{ meltsPkgs
, ...
} @ attrs:
let
  config = import ../../../makes/melts/config attrs.copy;
  makeEntrypoint = import ../../../makes/utils/make-entrypoint meltsPkgs;
in
makeEntrypoint {
  arguments = {
    envSetupMeltsRuntime = config.setupMeltsRuntime;
  };
  location = "/bin/melts";
  name = "melts-bin";
  template = ../../../makes/melts/bin/entrypoint.sh;
}
