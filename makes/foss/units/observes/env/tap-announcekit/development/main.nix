{ makePythonPypiEnvironment
, makeTemplate
, outputs
, ...
}:
makeTemplate {
  name = "observes-env-tap-announcekit-development";
  searchPaths = {
    source = [
      (makePythonPypiEnvironment {
        name = "observes-env-tap-announcekit-development";
        sourcesYaml = ./pypi-sources.yaml;
      })
      outputs."/observes/env/tap-announcekit/runtime"
    ];
  };
}
