{ inputs
, makePythonPypiEnvironment
, makeSearchPaths
, projectPath
, ...
}:
let
  self = projectPath inputs.observesIndex.common.singerIO;
  py_env = makePythonPypiEnvironment {
    name = "observes-singer-io-run-env";
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
