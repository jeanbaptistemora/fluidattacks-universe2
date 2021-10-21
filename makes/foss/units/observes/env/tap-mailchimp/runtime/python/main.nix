{ makePythonPypiEnvironment
, ...
}:
makePythonPypiEnvironment {
  name = "observes-env-tap-mailchimp-runtime-python";
  sourcesYaml = ./pypi-sources.yaml;
}
