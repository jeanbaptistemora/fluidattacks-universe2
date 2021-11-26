{ makeTemplate
, makePythonPypiEnvironment
, outputs
, ...
}:
makeTemplate {
  name = "observes-etl-code-env-development";
  searchPaths = {
    source = [
      (makePythonPypiEnvironment {
        name = "observes-etl-code-env-development";
        sourcesYaml = ./pypi-sources.yaml;
      })
      outputs."/observes/etl/code/env/runtime"
    ];
  };
}
