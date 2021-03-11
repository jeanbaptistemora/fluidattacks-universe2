{ buildPythonPackage
, buildPythonRequirements
, makeTemplate
, nixpkgs
, packages
, path
, ...
}:
let
  pythonRequirements = buildPythonRequirements {
    name = "timedoctor-tokens-env-development-python";
    requirements = {
      direct = [
        "click==7.1.2"
        "urllib3==1.26.3"
      ];
      inherited = [ ];
    };
    python = nixpkgs.python38;
  };
  self = buildPythonPackage {
    name = "observes-timedoctor-tokens";
    packagePath = path "/observes/services/timedoctor_tokens";
    python = nixpkgs.python38;
  };
in
makeTemplate {
  name = "observes-env-development-timedoctor-tokens";
  searchPaths = {
    envPaths = [
      packages.observes.bin.update-project-variable
      pythonRequirements
      self
    ];
    envPython38Paths = [
      pythonRequirements
      self
    ];
  };
}
