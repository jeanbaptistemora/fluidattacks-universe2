{ makePythonPypiEnvironment
, makeSearchPaths
, projectPath
, ...
}:
let
  self = projectPath "/observes/common/utils_logger";
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
