{ inputs
, makePythonPypiEnvironment
, makeTemplate
, outputs
, projectPath
, ...
}:
let
  self = projectPath inputs.observesIndex.tap.bugsnag.root;
in
makeTemplate {
  name = "observes-singer-tap-bugsnag-env-runtime";
  searchPaths = {
    pythonMypy = [
      self
    ];
    pythonPackage = [
      self
    ];
    source = [
      (makePythonPypiEnvironment {
        name = "observes-singer-tap-bugsnag-env-runtime";
        sourcesYaml = ./pypi-sources.yaml;
      })
      outputs."/observes/common/paginator/env/runtime"
      outputs."/observes/common/singer-io/env/runtime"
      outputs."/observes/env/utils-logger/runtime"
    ];
  };
}
