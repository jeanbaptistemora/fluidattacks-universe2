{ makePythonPypiEnvironment
, makeTemplate
, inputs
, projectPath
, ...
}:
let
  self = projectPath "/observes/singer/tap_delighted";
in
makeTemplate {
  name = "observes-env-tap-delighted-runtime";
  searchPaths = {
    pythonMypy = [
      self
    ];
    pythonPackage = [
      self
    ];
    source = [
      (makePythonPypiEnvironment {
        name = "observes-env-tap-delighted-runtime";
        sourcesYaml = ./pypi-sources.yaml;
      })
      inputs.product.observes-env-paginator-runtime
      inputs.product.observes-env-singer-io-runtime
      inputs.product.observes-env-utils-logger-runtime
    ];
  };
}
