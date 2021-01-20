{ path
, skimsPkgs
, ...
} @ attrs:
let
  config = import (path "/makes/skims/config") attrs.copy;
  makeEntrypoint = import (path "/makes/utils/make-entrypoint") skimsPkgs;
in
makeEntrypoint {
  arguments = {
    envSetupSkimsRuntime = config.setupSkimsRuntime;
  };
  location = "/bin/skims";
  name = "skims-bin";
  template = (path "/makes/skims/bin/entrypoint.sh");
}
