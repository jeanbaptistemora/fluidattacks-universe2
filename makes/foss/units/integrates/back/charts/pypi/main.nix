{ makePythonPypiEnvironment
, ...
}:
makePythonPypiEnvironment {
  name = "integrates-back-charts-pypi";
  sourcesYaml = ./pypi-sources.yaml;
}
