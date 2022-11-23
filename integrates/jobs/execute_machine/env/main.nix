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
      inputs.nixpkgs.jq
      inputs.nixpkgs.findutils
    ];
  };
  sourcesYaml = ./pypi-sources.yaml;
}
