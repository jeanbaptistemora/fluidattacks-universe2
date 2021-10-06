{ makePythonPypiEnvironment
, ...
}:
makePythonPypiEnvironment {
  name = "integrates-web-e2e-pypi";
  sourcesYaml = ./pypi-sources.yaml;
}
