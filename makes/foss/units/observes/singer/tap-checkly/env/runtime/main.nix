{ makePythonPypiEnvironment
, makeTemplate
, outputs
, projectPath
, ...
}:
let
  self = projectPath "/observes/singer/tap_checkly";
in
makeTemplate {
  name = "observes-singer-tap-checkly-env-runtime";
  searchPaths = {
    pythonMypy = [
      self
    ];
    pythonPackage = [
      self
    ];
    source = [
      (makePythonPypiEnvironment {
        name = "observes-singer-tap-checkly-env-runtime";
        sourcesYaml = ./pypi-sources.yaml;
      })
      outputs."/observes/env/paginator/runtime"
      outputs."/observes/common/purity/env/runtime"
      outputs."/observes/common/singer-io/env/runtime"
      outputs."/observes/env/utils-logger/runtime"
    ];
  };
}
