{makePythonPypiEnvironment, ...}:
makePythonPypiEnvironment {
  name = "melts-config-type-stubs";
  sourcesYaml = ./pypi-sources.yaml;
}
