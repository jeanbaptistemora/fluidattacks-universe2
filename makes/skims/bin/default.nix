{ skimsPkgs
, ...
} @ attrs:
let
  config = import ../../../makes/skims/config attrs.copy;
  makeEntrypoint = import ../../../makes/utils/make-entrypoint skimsPkgs;
in
makeEntrypoint {
  arguments = {
    envSetupSkimsRuntime = config.setupSkimsRuntime;
  };
  location = "/bin/skims";
  name = "skims-bin";
  template = ../../../makes/skims/bin/entrypoint.sh;
}
