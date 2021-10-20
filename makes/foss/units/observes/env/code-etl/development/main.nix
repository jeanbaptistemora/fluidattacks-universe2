{ inputs
, makeTemplate
, makePythonPypiEnvironment
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
      inputs.product.observes-env-code-etl-runtime
    ];
  };
}
