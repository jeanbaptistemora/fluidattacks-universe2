{ inputs
, makePythonPypiEnvironment
, makeSearchPaths
, outputs
, projectPath
, ...
}:
let
  self = projectPath inputs.observesIndex.taps.announcekit;
  py_env = makePythonPypiEnvironment {
    name = "observes-env-tap-announcekit-runtime";
    sourcesYaml = ./pypi-sources.yaml;
  };
in
makeSearchPaths {
  pythonMypy = [
    self
  ];
  pythonPackage = [
    self
  ];
  source = [
    py_env
    outputs."/observes/common/paginator/env/runtime"
    outputs."/observes/common/singer-io/env/runtime"
    outputs."/observes/common/utils-logger/runtime"
  ];
}
