{ makePythonPypiEnvironment
, makeTemplate
, outputs
, ...
}:
makeTemplate {
  name = "observes-env-singer-io-development";
  searchPaths = {
    source = [
      (makePythonPypiEnvironment {
        name = "observes-env-singer-io-runtime";
        sourcesYaml = ./pypi-sources.yaml;
      })
      outputs."/observes/env/singer-io/runtime"
    ];
  };
}
