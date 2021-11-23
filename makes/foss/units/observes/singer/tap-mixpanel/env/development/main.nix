{ makePythonPypiEnvironment
, makeTemplate
, outputs
, ...
}:
makeTemplate {
  name = "observes-singer-tap-mixpanel-env-development";
  searchPaths = {
    source = [
      (makePythonPypiEnvironment {
        name = "observes-singer-tap-mixpanel-env-development";
        sourcesYaml = ./pypi-sources.yaml;
      })
      outputs."/observes/singer/tap-mixpanel/env/runtime"
    ];
  };
}
