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
    envPython = "${skimsPkgs.python38}/bin/python3.8";
    envSetupSkimsRuntime = config.setupSkimsRuntime;
  };
  location = "/bin/skims-repl";
  name = "skims-repl";
  template = (path "/makes/skims/bin-repl/entrypoint.sh");
}
