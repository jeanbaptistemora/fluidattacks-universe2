{ makePythonPypiEnvironment
, ...
}:
makePythonPypiEnvironment {
  name = "observes-paginator-run-env";
  sourcesYaml = ./pypi-sources.yaml;
}
