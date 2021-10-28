{ makeTemplate
, makePythonPypiEnvironment
, outputs
, projectPath
, ...
}:
let
  pythonRequirements = makePythonPypiEnvironment {
    name = "integrates-back-runtime";
    sourcesYaml = ./pypi-sources.yaml;
    withSetuptools_57_4_0 = true;
    withWheel_0_37_0 = true;
  };
in
makeTemplate {
  name = "integrates-back-pypi-runtime";
  searchPaths = {
    pythonPackage = [
      (projectPath "/integrates/back/src")
      (projectPath "/integrates")
    ];
    source = [
      pythonRequirements
      outputs."/makes/python/safe-pickle"
    ];
  };
}
