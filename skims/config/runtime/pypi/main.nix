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
      inputs.nixpkgs.gnutar
      inputs.nixpkgs.gzip
      inputs.nixpkgs.python38Packages.pycurl
    ];
    pythonPackage38 = [
      inputs.nixpkgs.python38Packages.pygraphviz
      inputs.nixpkgs.python38Packages.pycurl
    ];
  };
  searchPathsRuntime = searchPathsBuild;
  sourcesYaml = ./sources.yaml;
  withSetuptools_57_4_0 = true;
  withWheel_0_37_0 = true;
}
