{ makes
, makeEntrypoint
, packages
, path
, ...
}:
let
  pythonRequirements = makes.makePythonPypiEnvironment {
    name = "integrates-back-test-functional";
    sourcesYaml = ./pypi-sources.yaml;
  };
in
makeEntrypoint {
  arguments = {
    envIntegratesEnv = packages.integrates.back.env;
  };
  name = "integrates-back-test-functional";
  searchPaths = {
    envPaths = [
      packages.integrates.cache
      packages.integrates.db
      packages.integrates.storage
    ];
    envSources = [
      pythonRequirements
    ];
  };
  template = path "/makes/applications/integrates/back/test/functional/entrypoint.sh";
}
