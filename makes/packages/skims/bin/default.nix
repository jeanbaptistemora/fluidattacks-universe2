{ path
, skimsPkgs
, ...
} @ attrs:
let
  makeEntrypoint = import (path "/makes/utils/make-entrypoint") path skimsPkgs;
in
makeEntrypoint {
  arguments = {
    envSetupSkimsRuntime = import (path "/makes/packages/skims/config-runtime") attrs.copy;
  };
  name = "skims";
  template = path "/makes/packages/skims/bin/entrypoint.sh";
}
