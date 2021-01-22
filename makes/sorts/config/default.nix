{ outputs
, path
, sortsPkgs
, ...
} @ _:
let
  makeSearchPaths = import (path "/makes/utils/make-search-paths") path sortsPkgs;
  makeTemplate = import (path "/makes/utils/make-template") path sortsPkgs;
  nixRequirements = makeSearchPaths [ sortsPkgs.gcc.cc ];
in
{
  setupSortsDevelopment = makeTemplate {
    arguments = {
      envBinPath = nixRequirements.binPath;
      envLibPath = nixRequirements.libPath;
      envPyPath = nixRequirements.pyPath;
      envPythonRequirements = outputs.packages.sorts-config-python-requirements-development;
      envUtilsBashLibPython = path "/makes/utils/bash-lib/python.sh";
    };
    name = "sorts-config-setup-sorts-development";
    template = path "/makes/sorts/config/setup-sorts-development.sh";
  };

  setupSortsRuntime = makeTemplate {
    arguments = {
      envContextFile = makeTemplate {
        arguments = {
          envSortsModel = sortsPkgs.fetchurl {
            url = "https://sorts.s3.amazonaws.com/training-output/model.joblib?versionId=IKhqYYxpu72milhmPGti94p.YvdyJxzV";
            sha256 = "0h9yYuNI2L4V6dzfhYgoE55lFrg21B2D0NJT3U6Z9aY=";
          };
          envSrcSortsStatic = path "/sorts/static";
        };
        name = "sorts-config-context-file";
        template = ''
          export SORTS_STATIC_PATH='__envSrcSortsStatic__'
          export SORTS_MODEL_PATH='__envSortsModel__'
        '';
      };
      envPython = "${sortsPkgs.python38}/bin/python";
      envPythonRequirements = outputs.packages.sorts-config-python-requirements-runtime;
      envBinPath = nixRequirements.binPath;
      envLibPath = nixRequirements.libPath;
      envPyPath = nixRequirements.pyPath;
      envSrcSortsSorts = path "/sorts/sorts";
      envUtilsBashLibPython = path "/makes/utils/bash-lib/python.sh";
    };
    name = "sorts-config-setup-sorts-runtime";
    template = path "/makes/sorts/config/setup-sorts-runtime.sh";
  };
}
