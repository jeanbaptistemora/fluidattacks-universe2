{makePythonPypiEnvironment, ...}:
makePythonPypiEnvironment {
  name = "sorts-env-type-stubs";
  sourcesYaml = ./pypi-sources.yaml;
}
