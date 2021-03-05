{ nixpkgs
, path
, ...
}:
let
  buildPythonPackage = import (path "/makes/utils/build-python-package") path nixpkgs;
  makeEntrypoint = import (path "/makes/utils/make-entrypoint") path nixpkgs;
in
makeEntrypoint {
  arguments = {
    envBashLibPython = path "/makes/utils/python/template.sh";
    envTapJson = buildPythonPackage {
      dependencies = [ ];
      name = "observes-bin-tap-json";
      packagePath = path "/observes/singer/tap_json";
      python = nixpkgs.python37;
    };
  };
  name = "observes-tap-json";
  template = path "/makes/applications/observes/tap-json/entrypoint.sh";
}
