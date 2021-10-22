{ makePythonPypiEnvironment
, makeTemplate
, inputs
, outputs
, projectPath
, ...
}:
let
  self = projectPath "/observes/singer/tap_checkly";
in
makeTemplate {
  name = "observes-env-tap-checkly-runtime";
  searchPaths = {
    pythonMypy = [
      self
    ];
    pythonPackage = [
      self
    ];
    source = [
      (makePythonPypiEnvironment {
        name = "observes-env-tap-checkly-runtime";
        sourcesYaml = ./pypi-sources.yaml;
      })
      outputs."/observes/env/paginator/runtime"
      inputs.product.observes-env-singer-io-runtime
      inputs.product.observes-env-utils-logger-runtime
    ];
  };
}
