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
    envSetupForcesDevelopment = config.setupForcesDevelopment;
  };
  location = "/bin/forces-test";
  name = "forces-test";
  template = ../../../makes/forces/test/entrypoint.sh;
}
