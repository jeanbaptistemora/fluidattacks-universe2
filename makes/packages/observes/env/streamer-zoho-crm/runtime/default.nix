{ makes
, makeTemplate
, packages
, path
, ...
}:
let
  self = path "/observes/singer/streamer_zoho_crm";
in
makeTemplate {
  name = "observes-env-streamer-zoho-crm-runtime";
  searchPaths = {
    envMypyPaths = [
      self
    ];
    envPythonPaths = [
      self
    ];
    envSources = [
      (makes.makePythonPypiEnvironment {
        name = "observes-env-streamer-zoho-crm-runtime";
        sourcesYaml = ./pypi-sources.yaml;
      })
      packages.observes.env.postgres-client.runtime
      packages.observes.env.singer-io.runtime
      packages.observes.env.utils-logger.runtime
    ];
  };
}
