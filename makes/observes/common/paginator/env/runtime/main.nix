{ makePythonPypiEnvironment
, ...
}:
makePythonPypiEnvironment {
  name = "observes-paginator-dev-env";
  sourcesYaml = ./pypi-sources.yaml;
}
