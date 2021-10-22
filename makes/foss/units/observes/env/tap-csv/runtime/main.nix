{ makePythonPypiEnvironment
, makeTemplate
, outputs
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
      outputs."/observes/env/singer-io/runtime"
      outputs."/observes/env/purity/runtime"
    ];
  };
}
