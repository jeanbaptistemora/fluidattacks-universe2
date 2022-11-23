{makePythonPypiEnvironment, ...}:
makePythonPypiEnvironment {
  name = "observes-common-singer-io-env-type-stubs";
  sourcesYaml = ./pypi-sources.yaml;
}
