{
  makePythonPypiEnvironment,
  inputs,
  ...
}:
makePythonPypiEnvironment {
  name = "report";
  searchPathsRuntime = {
    bin = [
      inputs.nixpkgs.git
    ];
  };
  sourcesYaml = ./pypi-sources.yaml;
}
