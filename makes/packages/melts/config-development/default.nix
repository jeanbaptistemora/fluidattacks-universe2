{ makes
, makeTemplate
, nixpkgs
, ...
}:
let
  pythonRequirements = makes.makePythonPypiEnvironment {
    name = "melts-development";
    sourcesYaml = ./pypi-sources.yaml;
  };
in
makeTemplate {
  name = "melts-config-development";
  searchPaths = {
    envPaths = [ nixpkgs.docker ];
    envSources = [ pythonRequirements ];
  };
}
