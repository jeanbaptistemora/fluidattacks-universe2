{ makePythonPypiEnvironment
, ...
}:
makePythonPypiEnvironment {
  name = "forces-development";
  sourcesYaml = ./pypi-sources.yaml;
}
