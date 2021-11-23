{ makePythonPypiEnvironment
, makeTemplate
, outputs
, ...
}:
makeTemplate {
  name = "observes-singer-tap-csv-env-development";
  searchPaths = {
    source = [
      (makePythonPypiEnvironment {
        name = "observes-singer-tap-csv-env-development";
        sourcesYaml = ./pypi-sources.yaml;
      })
      outputs."/observes/singer/tap-csv/env/runtime"
    ];
  };
}
