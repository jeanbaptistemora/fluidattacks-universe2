{ inputs
, makePythonPypiEnvironment
, makeSearchPaths
, projectPath
, ...
}:
let
  self = projectPath inputs.observesIndex.common.paginator;
  py_env = makePythonPypiEnvironment {
    name = "observes-paginator-run-env";
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
