{ makes
, makeTemplate
, packages
, ...
}:
with packages.observes.env;
makeTemplate {
  name = "observes-env-singer-io-development";
  searchPaths = {
    envSources = [
      (makes.makePythonPypiEnvironment {
        name = "observes-env-singer-io-runtime";
        sourcesYaml = ./pypi-sources.yaml;
      })
      singer-io.runtime
    ];
  };
}
