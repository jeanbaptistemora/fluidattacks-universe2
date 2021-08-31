{ makeTemplate
, makes
, packages
, ...
}:
makeTemplate {
  name = "observes-env-tap-mailchimp-development";
  searchPaths = {
    envSources = [
      (makes.makePythonPypiEnvironment {
        name = "observes-env-tap-mailchimp-development";
        sourcesYaml = ./pypi-sources.yaml;
      })
      packages.observes.env.tap-mailchimp.runtime
    ];
  };
}
