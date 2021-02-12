{ path
, sortsPkgs
, ...
} @ _:
let
  buildPythonRequirements = import (path "/makes/utils/build-python-requirements") path sortsPkgs;
  makeSearchPaths = import (path "/makes/utils/make-search-paths-deprecated") path sortsPkgs;
  makeTemplate = import (path "/makes/utils/make-template") path sortsPkgs;
in
makeTemplate {
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
    envPythonRequirements = buildPythonRequirements {
      dependencies = [ ];
      name = "sorts-runtime";
      requirements = {
        direct = [
          "bugsnag==3.9.0"
          "category-encoders==2.2.2"
          "click==7.1.2"
          "GitPython==3.1.9"
          "gql==3.0.0a2"
          "joblib==0.16.0"
          "more-itertools==8.5.0"
          "mypy-extensions==0.4.3"
          "numpy==1.19.2"
          "pandas==1.1.2"
          "prettytable==1.0.1"
          "PyDriller==1.15.2"
          "pytz==2020.1"
          "requests==2.24.0"
          "scikit-learn==0.23.2"
          "tqdm==4.50.2"
        ];
        inherited = [
          "aiohttp==3.6.2"
          "async-timeout==3.0.1"
          "attrs==20.3.0"
          "certifi==2020.12.5"
          "chardet==3.0.4"
          "gitdb==4.0.5"
          "graphql-core==3.1.2"
          "idna==2.10"
          "lizard==1.17.7"
          "multidict==4.7.6"
          "patsy==0.5.1"
          "python-dateutil==2.8.1"
          "scipy==1.6.0"
          "six==1.15.0"
          "smmap==3.0.4"
          "statsmodels==0.12.1"
          "threadpoolctl==2.1.0"
          "urllib3==1.25.11"
          "wcwidth==0.2.5"
          "WebOb==1.8.6"
          "websockets==8.1"
          "yarl==1.6.3"
        ];
      };
      python = sortsPkgs.python38;
    };
    envSearchPaths = makeSearchPaths [ sortsPkgs.gcc.cc sortsPkgs.git ];
    envSrcSortsSorts = path "/sorts/sorts";
    envUtilsBashLibPython = path "/makes/utils/python/template.sh";
  };
  name = "sorts-config-runtime";
  template = path "/makes/packages/sorts/config-runtime/template.sh";
}
