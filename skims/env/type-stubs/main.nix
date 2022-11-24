{makePythonPypiEnvironment, ...}:
makePythonPypiEnvironment {
  name = "skims-env-type-stubs";
  sourcesYaml = ./pypi-sources.yaml;
}
