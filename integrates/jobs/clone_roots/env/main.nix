{
  makePythonPypiEnvironment,
  inputs,
  ...
}:
makePythonPypiEnvironment {
  name = "clone-roots";
  searchPathsRuntime = {
    bin = [
      inputs.nixpkgs.git
      inputs.nixpkgs.openssh
    ];
  };
  sourcesYaml = ./pypi-sources.yaml;
}
