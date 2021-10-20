{ inputs
, makePythonPypiEnvironment
, ...
}:
makePythonPypiEnvironment {
  name = "skims-runtime";
  searchPaths = {
    bin = [ inputs.nixpkgs.gcc ];
  };
  sourcesYaml = ./sources.yaml;
  withSetuptools_57_4_0 = true;
  withWheel_0_37_0 = true;
}
