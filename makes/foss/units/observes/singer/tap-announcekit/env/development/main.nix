{ makePythonPypiEnvironment
, makeTemplate
, outputs
, ...
}:
makeTemplate {
  name = "observes-singer-tap-announcekit-env-development";
  searchPaths = {
    source = [
      (makePythonPypiEnvironment {
        name = "observes-singer-tap-announcekit-env-development-python";
        sourcesYaml = ./pypi-sources.yaml;
      })
      outputs."/observes/singer/tap-announcekit/env/runtime"
    ];
  };
}
