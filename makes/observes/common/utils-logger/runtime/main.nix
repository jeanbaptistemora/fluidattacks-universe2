{ makePythonPypiEnvironment
, ...
}:
makePythonPypiEnvironment {
  name = "observes-utils-logger-env-run";
  sourcesYaml = ./pypi-sources.yaml;
}
