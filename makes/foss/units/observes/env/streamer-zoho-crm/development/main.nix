{ makePythonPypiEnvironment
, makeTemplate
, inputs
, ...
}:
makeTemplate {
  name = "observes-env-streamer-zoho-crm-development";
  searchPaths = {
    source = [
      (makePythonPypiEnvironment {
        name = "observes-env-streamer-zoho-crm-development";
        sourcesYaml = ./pypi-sources.yaml;
      })
      inputs.product.observes-env-streamer-zoho-crm-runtime
    ];
  };
}
