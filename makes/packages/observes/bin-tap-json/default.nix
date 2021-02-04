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
    envBashLibPython = path "/makes/utils/python/template.sh";
    envTapJson = buildPythonPackage {
      dependencies = [ ];
      name = "observes-bin-tap-json";
      packagePath = path "/observes/singer/tap_json";
      python = observesPkgs.python37;
    };
  };
  name = "observes-tap-json";
  template = path "/makes/packages/observes/bin-tap-json/entrypoint.sh";
}
