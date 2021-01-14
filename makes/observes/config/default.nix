{ outputs
, observesPkgs
, ...
} @ _:
let
  makeSearchPaths = import ../../../makes/utils/make-search-paths observesPkgs;
  makeTemplate = import ../../../makes/utils/make-template observesPkgs;
  nixRequirements = {
    target-redshift-runtime = makeSearchPaths [
      observesPkgs.postgresql
    ];
  };
in
{
  setupObservesTargetRedshiftRuntime = makeTemplate {
    arguments = {
      envPython = "${observesPkgs.python37}/bin/python";
      envPythonRequirements = outputs.packages.observes-config-python-requirements-target-redshift-runtime;
      envBinPath = nixRequirements.target-redshift-runtime.binPath;
      envLibPath = nixRequirements.target-redshift-runtime.libPath;
      envPyPath = nixRequirements.target-redshift-runtime.pyPath;
      envSrcObservesTargetRedshiftEntrypoint = ../../../observes/singer/target_redshift/target_redshift/__init__.py;
      envUtilsBashLibPython = ../../../makes/utils/bash-lib/python.sh;
    };
    name = "observes-config-setup-target-redshift-runtime";
    template = ../../../makes/observes/config/setup-target-redshift-runtime.sh;
  };
}
