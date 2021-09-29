{ makePythonPypiEnvironment
, ...
}:
makePythonPypiEnvironment {
  name = "skims-env-development";
  sourcesYaml = ./pypi-sources.yaml;
}
