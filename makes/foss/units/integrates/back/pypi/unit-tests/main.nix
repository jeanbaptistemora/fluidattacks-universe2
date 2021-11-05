{ makePythonPypiEnvironment
, inputs
, ...
}:
makePythonPypiEnvironment {
  name = "integrates-back-unit-tests";
  searchPathsBuild = {
    bin = [ inputs.nixpkgs.gcc ];
  };
  sourcesYaml = ./pypi-sources.yaml;
  withSetuptools_57_4_0 = true;
  withWheel_0_37_0 = true;
}
