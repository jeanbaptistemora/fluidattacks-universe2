{makePythonPypiEnvironment, ...}:
makePythonPypiEnvironment {
  name = "common-google-close-sessions-env";
  sourcesYaml = ./pypi-sources.yaml;
}
