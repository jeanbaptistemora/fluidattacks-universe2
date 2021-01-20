{ outputs
, observesPkgs
, path
, ...
} @ _:
let
  makeSearchPaths = import (path "/makes/utils/make-search-paths") path observesPkgs;
  makeTemplate = import (path "/makes/utils/make-template") path observesPkgs;
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
      envSrcObservesTargetRedshiftEntrypoint = path "/observes/singer/target_redshift/target_redshift/__init__.py";
      envUtilsBashLibPython = path "/makes/utils/bash-lib/python.sh";
    };
    name = "observes-config-setup-target-redshift-runtime";
    template = path "/makes/observes/config/setup-target-redshift-runtime.sh";
  };
  setupObservesStreamerZohoCrmRuntime = makeTemplate {
    arguments = {
      envPython = "${observesPkgs.python38}/bin/python";
      envPythonRequirements = outputs.packages.observes-config-python-requirements-streamer-zoho-crm-runtime;
      envBinPath = nixRequirements.streamer-zoho-crm-runtime.binPath;
      envLibPath = nixRequirements.streamer-zoho-crm-runtime.libPath;
      envPyPath = nixRequirements.streamer-zoho-crm-runtime.pyPath;
      envSrcObservesStreamerZohoCrmEntrypoint = path "/observes/singer/streamer_zoho_crm/streamer_zoho_crm/__init__.py";
      envUtilsBashLibPython = path "/makes/utils/bash-lib/python.sh";
    };
    name = "observes-config-setup-streamer-zoho-crm-runtime";
    template = path "/makes/observes/config/setup-streamer-zoho-crm-runtime.sh";
  };
}
