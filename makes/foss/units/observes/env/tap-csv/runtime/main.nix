{ inputs
, makePythonPypiEnvironment
, makeTemplate
, projectPath
, ...
}:
let
  self = projectPath "/observes/singer/tap_csv";
in
makeTemplate {
  name = "observes-env-tap-csv-runtime";
  searchPaths = {
    pythonMypy = [
      self
    ];
    pythonPackage = [
      self
    ];
    source = [
      (makePythonPypiEnvironment {
        name = "observes-env-tap-csv-runtime";
        sourcesYaml = ./pypi-sources.yaml;
      })
      inputs.product.observes-env-singer-io-runtime
      inputs.product.observes-env-purity-runtime
    ];
  };
}
