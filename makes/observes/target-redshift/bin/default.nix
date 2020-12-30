attrs @ {
  observesPkgs,
  ...
}:

let
  buildPythonPackage = import ../../../../makes/utils/build-python-package observesPkgs;
  makeEntrypoint = import ../../../../makes/utils/make-entrypoint observesPkgs;
in
  makeEntrypoint {
    arguments = {
      envBashLibPython = ../../../../makes/utils/bash-lib/python.sh;
      envTargetRedshift = buildPythonPackage {
        dependencies = [
          observesPkgs.postgresql
        ];
        packagePath = ../../../../observes/singer/target_redshift;
        python = observesPkgs.python37;
      };
    };
    location = "/bin/observes-target-redshift";
    name = "observes-target-redshift-bin";
    template = ../../../../makes/observes/target-redshift/bin/entrypoint.sh;
  }
