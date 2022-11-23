{makePythonPypiEnvironment, ...}:
makePythonPypiEnvironment {
  name = "integrates-env-type-stubs";
  sourcesYaml = ./pypi-sources.yaml;
}
