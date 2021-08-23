{ makeTemplate
, makes
, ...
}:
let
  pythonRequirements = makes.makePythonPypiEnvironment {
    name = "forces-development";
    sourcesYaml = ./pypi-sources.yaml;
  };
in
makeTemplate {
  name = "forces-config-development";
  searchPaths = {
    envSources = [ pythonRequirements ];
  };
}
