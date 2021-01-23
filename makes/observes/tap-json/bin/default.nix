{ observesPkgs
, path
, ...
} @ _:
let
  buildPythonPackage = import (path "/makes/utils/build-python-package") path observesPkgs;
  makeEntrypoint = import (path "/makes/utils/make-entrypoint") path observesPkgs;
in
makeEntrypoint {
  arguments = {
    envBashLibPython = path "/makes/utils/python.sh";
    envTapJson = buildPythonPackage {
      dependencies = [ ];
      packagePath = path "/observes/singer/tap_json";
      python = observesPkgs.python37;
    };
  };
  location = "/bin/observes-tap-json";
  name = "observes-tap-json-bin";
  template = path "/makes/observes/tap-json/bin/entrypoint.sh";
}
