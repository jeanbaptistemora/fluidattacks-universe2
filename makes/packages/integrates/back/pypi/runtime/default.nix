{ makes
, makeTemplate
, packages
, path
, ...
}:
let
  pythonRequirements = makes.makePythonPypiEnvironment {
    name = "integrates-back-runtime";
    sourcesYaml = ./sources.yaml;
    withSetuptools_57_4_0 = true;
    withWheel_0_37_0 = true;
  };
in
makeTemplate {
  name = "integrates-back-pypi-runtime";
  searchPaths = {
    envPythonPaths = [
      (path "/integrates/back/src")
      (path "/integrates")
    ];
    envSources = [
      pythonRequirements
      packages.makes.python.safe-pickle
    ];
  };
}
