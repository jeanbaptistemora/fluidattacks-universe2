{makePythonPypiEnvironment, ...}:
makePythonPypiEnvironment {
  name = "forces-config-typing-stubs";
  sourcesYaml = ./pypi-sources.yaml;
}
