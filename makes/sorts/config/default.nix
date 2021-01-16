{ outputs
, sortsPkgs
, ...
} @ _:
let
  makeSearchPaths = import ../../../makes/utils/make-search-paths sortsPkgs;
  makeTemplate = import ../../../makes/utils/make-template sortsPkgs;
  nixRequirements = {
    development = makeSearchPaths [ ];
    runtime = makeSearchPaths [ sortsPkgs.gcc.cc ];
  };
in
{
  setupSortsDevelopment = makeTemplate {
    arguments = {
      envBinPath = nixRequirements.development.binPath;
      envLibPath = nixRequirements.development.libPath;
      envPyPath = nixRequirements.development.pyPath;
      envPythonRequirements = outputs.packages.sorts-config-python-requirements-development;
      envUtilsBashLibPython = ../../../makes/utils/bash-lib/python.sh;
    };
    name = "sorts-config-setup-sorts-development";
    template = ../../../makes/sorts/config/setup-sorts-development.sh;
  };

  setupSortsRuntime = makeTemplate {
    arguments = {
      envContextFile = makeTemplate {
        arguments = {
          envSrcSortsStatic = ../../../sorts/static;
        };
        name = "sorts-config-context-file";
        template = ''
          export SORTS_STATIC='__envSrcSortsStatic__'
        '';
      };
      envPython = "${sortsPkgs.python38}/bin/python";
      envPythonRequirements = outputs.packages.sorts-config-python-requirements-runtime;
      envBinPath = nixRequirements.runtime.binPath;
      envLibPath = nixRequirements.runtime.libPath;
      envPyPath = nixRequirements.runtime.pyPath;
      envSrcSortsSorts = ../../../sorts/sorts;
      envUtilsBashLibPython = ../../../makes/utils/bash-lib/python.sh;
    };
    name = "sorts-config-setup-sorts-runtime";
    template = ../../../makes/sorts/config/setup-sorts-runtime.sh;
  };
}
