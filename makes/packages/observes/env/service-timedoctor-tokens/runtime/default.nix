{ makes
, makeTemplate
, packages
, path
, ...
}:
let
  self = path "/observes/services/timedoctor_tokens";
in
makeTemplate {
  name = "observes-env-service-timedoctor-tokens-runtime";
  searchPaths = {
    envMypyPaths = [
      self
    ];
    envPaths = [
      packages.observes.bin.update-project-variable
    ];
    envPythonPaths = [
      self
    ];
    envSources = [
      (makes.makePythonPypiEnvironment {
        name = "observes-env-service-timedoctor-tokens-runtime";
        sourcesYaml = ./pypi-sources.yaml;
      })
      packages.observes.env.utils-logger.runtime
    ];
  };
}
