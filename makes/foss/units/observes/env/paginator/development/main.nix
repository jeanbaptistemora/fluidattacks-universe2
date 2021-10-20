{ makePythonPypiEnvironment
, makeTemplate
, inputs
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
      inputs.product.observes-env-paginator-runtime
    ];
  };
}
