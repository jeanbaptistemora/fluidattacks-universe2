attrs @ {
  pkgsObserves,
  ...
}:

let
  buildPythonPackage = import ../../../../makes/utils/build-python-package pkgsObserves;
  makeEntrypoint = import ../../../../makes/utils/make-entrypoint pkgsObserves;
in
  makeEntrypoint {
    arguments = {
      envBashLibPython = ../../../../makes/utils/bash-lib/python.sh;
      envShell = "${pkgsObserves.bash}/bin/bash";
      envTapJson = buildPythonPackage {
        dependencies = [];
        packagePath = ../../../../observes/singer/tap_json;
        python = pkgsObserves.python37;
      };
    };
    location = "/bin/observes-tap-json";
    name = "observes-tap-json-bin";
    template = ../../../../makes/observes/tap-json/bin/entrypoint.sh;
  }
