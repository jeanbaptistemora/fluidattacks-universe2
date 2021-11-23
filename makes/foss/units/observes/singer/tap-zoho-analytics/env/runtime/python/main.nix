{ makePythonPypiEnvironment
, ...
}:
makePythonPypiEnvironment {
  name = "observes-singer-tap-zoho-env-analytics-runtime-python";
  sourcesYaml = ./pypi-sources.yaml;
}
