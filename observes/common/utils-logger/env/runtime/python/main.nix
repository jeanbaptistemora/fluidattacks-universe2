{makePythonPypiEnvironment, ...}:
makePythonPypiEnvironment {
  name = "observes-common-utils-logger-env-runtime-python";
  sourcesYaml = ./pypi-sources.yaml;
}
