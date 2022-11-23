{makePythonPypiEnvironment, ...}:
makePythonPypiEnvironment {
  name = "observes-singer-tap-json-env-type-stubs";
  sourcesYaml = ./pypi-sources.yaml;
}
