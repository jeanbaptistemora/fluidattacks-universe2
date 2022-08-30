{makePythonPypiEnvironment, ...}:
makePythonPypiEnvironment {
  name = "integrates-streams-runtime";
  sourcesYaml = ./pypi-sources.yaml;
}
