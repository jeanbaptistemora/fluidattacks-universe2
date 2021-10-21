{ makeTemplate
, makePythonPypiEnvironment
, outputs
, ...
}:
makeTemplate {
  name = "observes-env-tap-mailchimp-development";
  searchPaths = {
    source = [
      (makePythonPypiEnvironment {
        name = "observes-env-tap-mailchimp-development";
        sourcesYaml = ./pypi-sources.yaml;
      })
      outputs."/observes/env/tap-mailchimp/runtime"
    ];
  };
}
