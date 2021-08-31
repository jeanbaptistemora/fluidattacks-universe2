{ makes
, makeTemplate
, packages
, ...
}:
makeTemplate {
  name = "observes-env-streamer-zoho-crm-development";
  searchPaths = {
    envSources = [
      (makes.makePythonPypiEnvironment {
        name = "observes-env-streamer-zoho-crm-development";
        sourcesYaml = ./pypi-sources.yaml;
      })
      packages.observes.env.streamer-zoho-crm.runtime
    ];
  };
}
