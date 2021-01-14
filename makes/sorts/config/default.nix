{ outputs
, sortsPkgs
, ...
} @ _:
let
  makeSearchPaths = import ../../../makes/utils/make-search-paths sortsPkgs;
  makeTemplate = import ../../../makes/utils/make-template sortsPkgs;
  nixRequirements = makeSearchPaths [ ];
in
{
  setupSortsDevelopment = makeTemplate {
    arguments = {
      envBinPath = nixRequirements.binPath;
      envLibPath = nixRequirements.libPath;
      envPyPath = nixRequirements.pyPath;
      envPythonRequirements = outputs.packages.sorts-config-python-requirements-development;
      envUtilsBashLibPython = ../../../makes/utils/bash-lib/python.sh;
    };
    name = "sorts-config-setup-sorts-development";
    template = ../../../makes/sorts/config/setup-sorts-development.sh;
  };

  setupSortsRuntime = makeTemplate {
    arguments = {
      envPython = "${sortsPkgs.python38}/bin/python";
      envPythonRequirements = outputs.packages.sorts-config-python-requirements-runtime;
      envBinPath = nixRequirements.binPath;
      envLibPath = nixRequirements.libPath;
      envPyPath = nixRequirements.pyPath;
      envSrcSortsSorts = ../../../sorts/sorts;
      envUtilsBashLibPython = ../../../makes/utils/bash-lib/python.sh;
    };
    name = "sorts-config-setup-sorts-runtime";
    template = ../../../makes/sorts/config/setup-sorts-runtime.sh;
  };
}
