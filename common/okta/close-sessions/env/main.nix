{makePythonPypiEnvironment, ...}:
makePythonPypiEnvironment {
  name = "common-okta-close-sessions-env";
  sourcesYaml = ./pypi-sources.yaml;
}
