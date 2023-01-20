{
  inputs,
  makePythonPypiEnvironment,
  ...
}:
makePythonPypiEnvironment rec {
  name = "skims-runtime";
  searchPathsBuild = {
    bin = [
      inputs.nixpkgs.curl
      inputs.nixpkgs.gcc
    ];
    export = [
      ["CPATH" inputs.nixpkgs.graphviz "/include"]
      ["LIBRARY_PATH" inputs.nixpkgs.graphviz "/lib"]
    ];
  };
  searchPathsRuntime = searchPathsBuild;
  sourcesYaml = ./sources.yaml;
  withSetuptools_57_4_0 = true;
  withWheel_0_37_0 = true;
}
