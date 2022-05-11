{makePythonPypiEnvironment, ...}:
makePythonPypiEnvironment {
  name = "common-okta-schedule-close-sessions-env";
  sourcesYaml = ./pypi-sources.yaml;
}
