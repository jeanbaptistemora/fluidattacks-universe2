{ makePythonPypiEnvironment
, makeTemplate
, inputs
, projectPath
, ...
}:
let
  self = projectPath "/observes/singer/streamer_zoho_crm";
in
makeTemplate {
  name = "observes-env-streamer-zoho-crm-runtime";
  searchPaths = {
    pythonMypy = [
      self
    ];
    pythonPackage = [
      self
    ];
    source = [
      (makePythonPypiEnvironment {
        name = "observes-env-streamer-zoho-crm-runtime";
        sourcesYaml = ./pypi-sources.yaml;
      })
      inputs.product.observes-env-postgres-client-runtime
      inputs.product.observes-env-singer-io-runtime
      inputs.product.observes-env-utils-logger-runtime
    ];
  };
}
