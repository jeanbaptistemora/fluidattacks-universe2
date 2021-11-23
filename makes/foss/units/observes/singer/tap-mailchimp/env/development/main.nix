{ makeTemplate
, makePythonPypiEnvironment
, outputs
, ...
}:
makeTemplate {
  name = "observes-singer-tap-mailchimp-env-development";
  searchPaths = {
    source = [
      (makePythonPypiEnvironment {
        name = "observes-singer-tap-mailchimp-env-development";
        sourcesYaml = ./pypi-sources.yaml;
      })
      outputs."/observes/singer/tap-mailchimp/env/runtime"
    ];
  };
}
