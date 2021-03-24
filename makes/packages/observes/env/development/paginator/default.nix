{ buildPythonPackage
, buildPythonRequirements
, makeTemplate
, nixpkgs
, path
, ...
}:
let
  pythonRequirements = buildPythonRequirements {
    name = "observes-env-development-paginator-python";
    requirements = {
      direct = [
        "aioextensions==20.11.1621472"
        "pytest==6.2.2"
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
  self = buildPythonPackage {
    name = "observes-paginator";
    packagePath = path "/observes/common/paginator";
    python = nixpkgs.python38;
  };
in
makeTemplate {
  name = "observes-env-development-paginator";
  searchPaths = {
    envPaths = [
      pythonRequirements
      self
    ];
    envPython38Paths = [
      pythonRequirements
      self
    ];
    envMypy38Paths = [
      self
    ];
  };
}
