{ outputs
, sortsPkgs
, ...
} @ _:
let
  makeSearchPaths = import ../../../makes/utils/make-search-paths sortsPkgs;
  makeTemplate = import ../../../makes/utils/make-template sortsPkgs;
  nixRequirements = makeSearchPaths [ sortsPkgs.gcc.cc ];
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
      envContextFile = makeTemplate {
        arguments = {
          envSortsModel = sortsPkgs.fetchurl {
            url = "https://sorts.s3.amazonaws.com/training-output/model.joblib";
            sha256 = "kBfRo6Bofx73P3wBrtagSGYlIww9XxHR2iR7V09/K64=";
          };
          envSrcSortsStatic = ../../../sorts/static;
        };
        name = "sorts-config-context-file";
        template = ''
          export SORTS_STATIC='__envSrcSortsStatic__'
          export SORTS_MODEL_PATH='__envSortsModel__'
        '';
      };
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
