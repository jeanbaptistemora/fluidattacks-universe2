{ makePythonPypiEnvironment
, makeTemplate
, outputs
, ...
}:
makeTemplate {
  name = "observes-env-tap-csv-development";
  searchPaths = {
    source = [
      (makePythonPypiEnvironment {
        name = "observes-env-tap-csv-development";
        sourcesYaml = ./pypi-sources.yaml;
      })
      outputs."/observes/env/tap-csv/runtime"
    ];
  };
}
