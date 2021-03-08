{ buildPythonRequirements
, makeTemplate
, nixpkgs
, ...
}:
let
  pythonRequirements = buildPythonRequirements {
    dependencies = [ ];
    name = "forces-development";
    requirements = {
      direct = [
        "pytest-asyncio==0.14.0"
        "pytest-cov==2.10.0"
        "pytest==5.4.3"
      ];
      inherited = [
        "attrs==20.3.0"
        "coverage==5.3.1"
        "more-itertools==8.6.0"
        "packaging==20.8"
        "pluggy==0.13.1"
        "py==1.10.0"
        "pyparsing==2.4.7"
        "wcwidth==0.2.5"
      ];
    };
    python = nixpkgs.python38;
  };
in
makeTemplate {
  name = "forces-config-development";
  searchPaths = {
    envPaths = [ pythonRequirements ];
    envPython38Paths = [ pythonRequirements ];
  };
}
