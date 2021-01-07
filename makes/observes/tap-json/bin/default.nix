{ observesPkgs
, ...
} @ _:
let
  buildPythonPackage = import ../../../../makes/utils/build-python-package observesPkgs;
  makeEntrypoint = import ../../../../makes/utils/make-entrypoint observesPkgs;
in
makeEntrypoint {
  arguments = {
    envBashLibPython = ../../../../makes/utils/bash-lib/python.sh;
    envTapJson = buildPythonPackage {
      dependencies = [ ];
      packagePath = ../../../../observes/singer/tap_json;
      python = observesPkgs.python37;
    };
  };
  location = "/bin/observes-tap-json";
  name = "observes-tap-json-bin";
  template = ../../../../makes/observes/tap-json/bin/entrypoint.sh;
}
