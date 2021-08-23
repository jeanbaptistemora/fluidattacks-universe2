{ makeTemplate
, makes
, packages
, ...
}:
let
  pythonRequirements = makes.makePythonPypiEnvironment {
    name = "integrates-back-unit-tests";
    sourcesYaml = ./pypi-sources.yaml;
    withSetuptools_57_4_0 = true;
    withWheel_0_37_0 = true;
  };
in
makeTemplate {
  name = "integrates-back-pypi-unit-tests";
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
}
