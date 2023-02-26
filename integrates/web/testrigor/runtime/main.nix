{makePythonPypiEnvironment, ...}:
makePythonPypiEnvironment {
  name = "integrates-web-testrigor-runtime";
  sourcesYaml = ./pypi-sources.yaml;
}
