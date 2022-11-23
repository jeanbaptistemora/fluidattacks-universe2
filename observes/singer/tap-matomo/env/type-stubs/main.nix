{makePythonPypiEnvironment, ...}:
makePythonPypiEnvironment {
  name = "observes-singer-tap-matomo-env-type-stubs";
  sourcesYaml = ./pypi-sources.yaml;
}
