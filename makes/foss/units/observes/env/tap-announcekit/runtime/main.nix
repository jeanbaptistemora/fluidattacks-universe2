{ makePythonPypiEnvironment
, makeTemplate
, inputs
, projectPath
, ...
}:
let
  self = projectPath "/observes/singer/tap_announcekit";
in
makeTemplate {
  name = "observes-env-tap-announcekit-runtime";
  searchPaths = {
    pythonMypy = [
      self
    ];
    pythonPackage = [
      self
    ];
    source = [
      (makePythonPypiEnvironment {
        name = "observes-env-tap-announcekit-runtime";
        sourcesYaml = ./pypi-sources.yaml;
      })
      inputs.product.observes-env-paginator-runtime
      inputs.product.observes-env-purity-runtime
      inputs.product.observes-env-singer-io-runtime
      inputs.product.observes-env-utils-logger-runtime
    ];
  };
}
