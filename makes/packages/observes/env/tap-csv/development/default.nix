{ makes
, makeTemplate
, packages
, ...
}:
makeTemplate {
  name = "observes-env-tap-csv-development";
  searchPaths = {
    envSources = [
      (makes.makePythonPypiEnvironment {
        name = "observes-env-tap-csv-development";
        sourcesYaml = ./pypi-sources.yaml;
      })
      packages.observes.env.tap-csv.runtime
    ];
  };
}
