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
    envPython = "${skimsPkgs.python38}/bin/python3.8";
    envSetupSkimsRuntime = config.setupSkimsRuntime;
  };
  location = "/bin/skims-repl";
  name = "skims-repl";
  template = path "/makes/products/skims/bin-repl/entrypoint.sh";
}
