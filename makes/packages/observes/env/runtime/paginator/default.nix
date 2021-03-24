{ buildPythonPackage
, makeTemplate
, nixpkgs
, packages
, path
, ...
}:
let
  pythonRequirements = packages.observes.env.runtime.paginator.python;
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
