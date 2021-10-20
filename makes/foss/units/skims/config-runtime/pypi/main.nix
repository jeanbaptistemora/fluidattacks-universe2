{ inputs
, makePythonPypiEnvironment
, ...
}:
makePythonPypiEnvironment {
  name = "skims-runtime";
  searchPaths = {
    bin = [ inputs.nixpkgs.gcc ];
    pythonPackage38 = [ inputs.nixpkgs.python38Packages.pygraphviz ];
  };
  sourcesYaml = ./sources.yaml;
  withSetuptools_57_4_0 = true;
  withWheel_0_37_0 = true;
}
