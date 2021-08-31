{ makes
, makeTemplate
, packages
, ...
}:
makeTemplate {
  name = "observes-env-tap-announcekit-development";
  searchPaths = {
    envSources = [
      (makes.makePythonPypiEnvironment {
        name = "observes-env-tap-announcekit-development";
        sourcesYaml = ./pypi-sources.yaml;
      })
      packages.observes.env.tap-announcekit.runtime
    ];
  };
}
