{ makeTemplate
, makePythonPypiEnvironment
, outputs
, ...
}:
makeTemplate {
  name = "observes-env-code-etl-development";
  searchPaths = {
    source = [
      (makePythonPypiEnvironment {
        name = "observes-env-code-etl-development";
        sourcesYaml = ./pypi-sources.yaml;
      })
      outputs."/observes/env/code-etl/runtime"
    ];
  };
}
