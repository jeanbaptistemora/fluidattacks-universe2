{ makePythonPypiEnvironment
, makeTemplate
, outputs
, ...
}:
makeTemplate {
  name = "observes-env-paginator-development";
  searchPaths = {
    source = [
      (makePythonPypiEnvironment {
        name = "observes-env-paginator-development";
        sourcesYaml = ./pypi-sources.yaml;
      })
      outputs."/observes/env/paginator/runtime"
    ];
  };
}
