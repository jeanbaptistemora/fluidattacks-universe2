{ forcesPkgs
, ...
} @ attrs:
let
  config = import ../../../makes/forces/config attrs.copy;
  makeEntrypoint = import ../../../makes/utils/make-entrypoint forcesPkgs;
in
makeEntrypoint {
  arguments = {
    envSetupForcesRuntime = config.setupForcesRuntime;
  };
  location = "/bin/forces";
  name = "forces-bin";
  template = ../../../makes/forces/bin/entrypoint.sh;
}
