{ makePythonPypiEnvironment
, makeTemplate
, outputs
, projectPath
, ...
}:
let
  self = projectPath "/observes/singer/tap_announcekit";
in
makeTemplate {
  name = "observes-singer-tap-announcekit-env-runtime";
  searchPaths = {
    pythonMypy = [
      self
    ];
    pythonPackage = [
      self
    ];
    source = [
      (makePythonPypiEnvironment {
        name = "observes-singer-tap-announcekit-env-runtime-python";
        sourcesYaml = ./pypi-sources.yaml;
      })
      outputs."/observes/env/paginator/runtime"
      outputs."/observes/common/purity/env/runtime"
      outputs."/observes/env/singer-io/runtime"
      outputs."/observes/env/utils-logger/runtime"
    ];
  };
}
