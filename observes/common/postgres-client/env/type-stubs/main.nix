{makePythonPypiEnvironment, ...}:
makePythonPypiEnvironment {
  name = "observes-common-postgres-client-env-type-stubs";
  sourcesYaml = ./pypi-sources.yaml;
}
