{ buildPythonRequirements
, makeTemplate
, nixpkgs
, packages
, ...
}:
let
  pythonRequirements = buildPythonRequirements {
    name = "code-etl-env-development-python";
    requirements = {
      direct = [
        "pytest-asyncio==0.15.1"
        "pytest==6.2.3"
      ];
      inherited = [
        "attrs==20.3.0"
        "iniconfig==1.1.1"
        "packaging==20.9"
        "pluggy==0.13.1"
        "py==1.10.0"
        "pyparsing==2.4.7"
        "toml==0.10.2"
      ];
    };
    python = nixpkgs.python38;
  };
in
with packages.observes.env;
makeTemplate {
  name = "code-etl-env-development";
  searchPaths = {
    envPaths = [
      pythonRequirements
    ];
    envPython38Paths = [
      pythonRequirements
    ];
    envSources = [
      runtime.code-etl
    ];
  };
}
