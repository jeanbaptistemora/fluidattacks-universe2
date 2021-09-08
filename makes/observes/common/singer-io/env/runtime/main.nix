{ makePythonPypiEnvironment
, ...
}:
makePythonPypiEnvironment {
  name = "observes-singer-io-run-env";
  sourcesYaml = ./pypi-sources.yaml;
}

