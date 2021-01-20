{ sortsPkgs
, ...
} @ attrs:
let
  config = import ../../../makes/sorts/config attrs.copy;
  makeEntrypoint = import ../../../makes/utils/make-entrypoint sortsPkgs;
in
makeEntrypoint {
  arguments = {
    envSetupSortsRuntime = config.setupSortsRuntime;
  };
  location = "/bin/sorts";
  name = "sorts-bin";
  template = ../../../makes/sorts/bin/entrypoint.sh;
}
