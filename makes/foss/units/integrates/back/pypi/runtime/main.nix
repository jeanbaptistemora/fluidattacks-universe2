{ makeTemplate
, makePythonPypiEnvironment
, outputs
, projectPath
, inputs
, ...
}:
let
  pythonRequirements = makePythonPypiEnvironment {
    name = "integrates-back-runtime";
    sourcesYaml = ./pypi-sources.yaml;
    searchPathsBuild = {
      bin = [ inputs.nixpkgs.gcc ];
    };
    searchPathsRuntime = {
      bin = [ inputs.nixpkgs.gcc ];
    };
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
      (projectPath "/makes/foss/units/bugsnag-client")
    ];
    source = [
      pythonRequirements
      outputs."/makes/python/safe-pickle"
    ];
  };
}
