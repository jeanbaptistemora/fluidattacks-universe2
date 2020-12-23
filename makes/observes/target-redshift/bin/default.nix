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
      envTargetRedshift = buildPythonPackage {
        dependencies = [
          pkgsObserves.postgresql
        ];
        packagePath = ../../../../observes/singer/target_redshift;
        python = pkgsObserves.python37;
      };
    };
    location = "/bin/observes-target-redshift";
    name = "observes-target-redshift-bin";
    template = ../../../../makes/observes/target-redshift/bin/entrypoint.sh;
  }
