{ makePythonPypiEnvironment
, makeTemplate
, outputs
, projectPath
, ...
}:
let
  self = projectPath "/observes/singer/tap_json";
in
makeTemplate {
  name = "observes-singer-tap-json-env-runtime";
  searchPaths = {
    pythonMypy = [
      self
    ];
    pythonPackage = [
      self
    ];
    source = [
      (makePythonPypiEnvironment {
        name = "observes-singer-tap-json-env-runtime";
        sourcesYaml = ./pypi-sources.yaml;
      })
      outputs."/observes/env/singer-io/runtime"
      outputs."/observes/env/utils-logger/runtime"
    ];
  };
}
