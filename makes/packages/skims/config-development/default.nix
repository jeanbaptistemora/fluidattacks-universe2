{ makes
, makeTemplate
, path
, ...
}:
let
  pythonRequirements = makes.makePythonPypiEnvironment {
    name = "skims-development";
    sourcesYaml = ./pypi-sources.yaml;
  };
in
makeTemplate {
  name = "skims-config-development";
  searchPaths = {
    envSources = [ pythonRequirements ];
  };
  template = path "/makes/packages/skims/config-development/template.sh";
}
