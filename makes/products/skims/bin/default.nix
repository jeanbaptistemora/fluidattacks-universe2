{ path
, skimsPkgs
, ...
} @ attrs:
let
  config = import (path "/makes/products/skims/config") attrs.copy;
  makeEntrypoint = import (path "/makes/utils/make-entrypoint") path skimsPkgs;
in
makeEntrypoint {
  arguments = {
    envSetupSkimsRuntime = config.setupSkimsRuntime;
  };
  location = "/bin/skims";
  name = "skims-bin";
  template = path "/makes/products/skims/bin/entrypoint.sh";
}
