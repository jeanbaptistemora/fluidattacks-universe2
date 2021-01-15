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
    streamer-zoho-crm-runtime = makeSearchPaths [
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
  setupObservesStreamerZohoCrmRuntime = makeTemplate {
    arguments = {
      envPython = "${observesPkgs.python38}/bin/python";
      envPythonRequirements = outputs.packages.observes-config-python-requirements-streamer-zoho-crm-runtime;
      envBinPath = nixRequirements.streamer-zoho-crm-runtime.binPath;
      envLibPath = nixRequirements.streamer-zoho-crm-runtime.libPath;
      envPyPath = nixRequirements.streamer-zoho-crm-runtime.pyPath;
      envSrcObservesStreamerZohoCrmEntrypoint = ../../../observes/singer/streamer_zoho_crm/streamer_zoho_crm/__init__.py;
      envUtilsBashLibPython = ../../../makes/utils/bash-lib/python.sh;
    };
    name = "observes-config-setup-streamer-zoho-crm-runtime";
    template = ../../../makes/observes/config/setup-streamer-zoho-crm-runtime.sh;
  };
}
