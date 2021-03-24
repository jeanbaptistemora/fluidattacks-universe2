{ buildPythonPackage
, buildPythonRequirements
, makeTemplate
, nixpkgs
, path
, ...
}:
let
  pythonRequirements = buildPythonRequirements {
    name = "observes-env-runtime-paginator-python";
    requirements = {
      direct = [
        "aioextensions==20.11.1621472"
      ];
      inherited = [ ];
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
  name = "observes-env-runtime-paginator";
  searchPaths = {
    envPaths = [
      pythonRequirements
      self
    ];
    envPython38Paths = [
      pythonRequirements
      self
    ];
  };
}
