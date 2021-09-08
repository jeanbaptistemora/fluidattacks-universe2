{ inputs
, makePythonPypiEnvironment
, makeSearchPaths
, projectPath
, ...
}:
let
  self = projectPath inputs.observesIndex.common.utilsLogger;
  py_env = makePythonPypiEnvironment {
    name = "observes-utils-logger-env-run";
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
  ];
}
