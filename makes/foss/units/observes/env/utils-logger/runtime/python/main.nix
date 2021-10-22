{ makePythonPypiEnvironment
, ...
}:
makePythonPypiEnvironment {
  name = "observes-env-utils-logger-runtime-python";
  sourcesYaml = ./pypi-sources.yaml;
}
