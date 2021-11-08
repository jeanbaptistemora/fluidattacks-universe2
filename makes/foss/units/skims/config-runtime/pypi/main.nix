{ inputs
, makePythonPypiEnvironment
, ...
}:
makePythonPypiEnvironment rec {
  name = "skims-runtime";
  searchPathsBuild = {
    bin = [ inputs.nixpkgs.gcc ];
    pythonPackage38 = [ inputs.nixpkgs.python38Packages.pygraphviz ];
  };
  searchPathsRuntime = searchPathsBuild;
  sourcesYaml = ./sources.yaml;
  withSetuptools_57_4_0 = true;
  withWheel_0_37_0 = true;
}
