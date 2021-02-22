{ integratesPkgs
, buildPythonRequirements
, makeEntrypoint
, packages
, path
, ...
} @ _:
let
  pythonRequirements = buildPythonRequirements integratesPkgs {
    name = "integrates-back-test-unit";
    requirements = {
      direct = [
        "aniso8601==9.0.0"
        "freezegun==0.3.15"
        "pytest-asyncio==0.12.0"
        "pytest-cov==2.9.0"
        "pytest==5.4.1"
      ];
      inherited = [
        "attrs==20.3.0"
        "coverage==5.4"
        "importlib-metadata==3.4.0"
        "more-itertools==8.7.0"
        "packaging==20.9"
        "pluggy==0.13.1"
        "py==1.10.0"
        "pyparsing==2.4.7"
        "python-dateutil==2.8.1"
        "six==1.15.0"
        "typing-extensions==3.7.4.3"
        "wcwidth==0.2.5"
        "zipp==3.4.0"
      ];
    };
    python = integratesPkgs.python37;
  };
in
makeEntrypoint integratesPkgs {
  arguments = {
    envIntegratesEnv = packages.integrates.back.env;
  };
  name = "integrates-back-test-unit";
  searchPaths = {
    envPaths = [
      packages.integrates.cache
      packages.integrates.db
      packages.integrates.storage
      pythonRequirements
    ];
    envPython37Paths = [
      pythonRequirements
    ];
    envUtils = [
      "/makes/utils/aws"
      "/makes/utils/sops"
    ];
  };
  template = path "/makes/applications/integrates/back/test/unit/entrypoint.sh";
}
