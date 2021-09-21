{ makes
, makeTemplate
, packages
, path
, ...
}:
let
  self = path "/observes/common/paginator";
in
makeTemplate {
  name = "observes-env-paginator-runtime";
  searchPaths = {
    envMypyPaths = [
      self
    ];
    envPythonPaths = [
      self
    ];
    envSources = [
      (makes.makePythonPypiEnvironment {
        name = "observes-env-paginator-runtime";
        sourcesYaml = ./pypi-sources.yaml;
      })
      packages.observes.env.purity.runtime
    ];
  };
}
