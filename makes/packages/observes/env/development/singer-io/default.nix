{ buildPythonPackage
, buildPythonRequirements
, makeTemplate
, nixpkgs
, path
, ...
}:
let
  pythonRequirements = buildPythonRequirements {
    name = "observes-env-development-singer-io-python";
    requirements = {
      direct = [
        "pytest==6.1.2"
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
    name = "observes-singer-io";
    packagePath = path "/observes/common/singer_io";
    python = nixpkgs.python38;
  };
in
makeTemplate {
  name = "observes-env-development-singer-io";
  searchPaths = {
    envPython38Paths = [
      pythonRequirements
      self
    ];
  };
}
