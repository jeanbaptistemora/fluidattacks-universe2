{makePythonPypiEnvironment, ...}:
makePythonPypiEnvironment {
  name = "common-okta-login";
  sourcesYaml = ./pypi-sources.yaml;
}
