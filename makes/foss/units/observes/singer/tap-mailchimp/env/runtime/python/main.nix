{ makePythonPypiEnvironment
, ...
}:
makePythonPypiEnvironment {
  name = "observes-singer-tap-mailchimp-env-runtime-python";
  sourcesYaml = ./pypi-sources.yaml;
}
