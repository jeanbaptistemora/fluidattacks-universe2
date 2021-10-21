{ inputs
, makePythonPypiEnvironment
, makeTemplate
, ...
}:
makeTemplate {
  name = "observes-env-singer-io-development";
  searchPaths = {
    source = [
      (makePythonPypiEnvironment {
        name = "observes-env-singer-io-runtime";
        sourcesYaml = ./pypi-sources.yaml;
      })
      inputs.product.observes-env-singer-io-runtime
    ];
  };
}
