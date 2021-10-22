{ makePythonPypiEnvironment
, ...
}:
makePythonPypiEnvironment {
  name = "observes-env-tap-zoho-analytics-runtime-python";
  sourcesYaml = ./pypi-sources.yaml;
}
