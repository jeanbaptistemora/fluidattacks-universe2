attrs @ {
  skimsPkgs,
  ...
}:

let
  config = import ../../../makes/skims/config attrs.copy;
  makeEntrypoint = import ../../../makes/utils/make-entrypoint skimsPkgs;
in
  makeEntrypoint {
    arguments = {
      envPython = "${skimsPkgs.python38}/bin/python3.8";
      envSetupSkimsRuntime = config.setupSkimsRuntime;
    };
    location = "/bin/skims-repl";
    name = "skims-repl";
    template = ../../../makes/skims/bin-repl/entrypoint.sh;
  }
