{ makePythonPypiEnvironment
, makeTemplate
, inputs
, ...
}:
makeTemplate {
  name = "observes-env-postgres-client-development";
  searchPaths = {
    source = [
      (makePythonPypiEnvironment {
        name = "observes-env-postgres-client-development";
        sourcesYaml = ./pypi-sources.yaml;
      })
      inputs.product.observes-env-postgres-client-runtime
    ];
  };
}
