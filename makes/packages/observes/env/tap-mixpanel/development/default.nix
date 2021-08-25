{ makes
, makeTemplate
, packages
, ...
}:
makeTemplate {
  name = "observes-env-tap-mixpanel-development";
  searchPaths = {
    envSources = [
      (makes.makePythonPypiEnvironment {
        name = "observes-env-tap-mixpanel-development";
        sourcesYaml = ./pypi-sources.yaml;
      })
      packages.observes.env.tap-mixpanel.runtime
    ];
  };
}
