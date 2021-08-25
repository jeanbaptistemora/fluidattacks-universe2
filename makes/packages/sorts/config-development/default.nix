{ makeTemplate
, makes
, nixpkgs
, path
, ...
}:
let
  pythonRequirements = makes.makePythonPypiEnvironment {
    name = "sorts-development";
    searchPaths.bin = [ nixpkgs.gcc nixpkgs.postgresql ];
    sourcesYaml = ./pypi-sources.yaml;
  };
in
makeTemplate {
  name = "sorts-config-development";
  searchPaths = {
    envLibraries = [ nixpkgs.gcc.cc.lib ];
    envPythonPaths = [
      (path "/sorts/training")
    ];
    envSources = [ pythonRequirements ];
  };
}
