{ makePythonPypiEnvironment
, makeTemplate
, outputs
, ...
}:
makeTemplate {
  name = "observes-env-tap-mixpanel-development";
  searchPaths = {
    source = [
      (makePythonPypiEnvironment {
        name = "observes-env-tap-mixpanel-development";
        sourcesYaml = ./pypi-sources.yaml;
      })
      outputs."/observes/env/tap-mixpanel/runtime"
    ];
  };
}
