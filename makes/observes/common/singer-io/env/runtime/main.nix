{ makePythonPypiEnvironment
, makeSearchPaths
, projectPath
, ...
}:
let
  self = projectPath "/observes/common/singer_io";
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
