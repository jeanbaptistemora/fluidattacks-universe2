{
  inputs,
  makePythonPypiEnvironment,
  makeScript,
  projectPath,
  ...
}:
makeScript {
  name = "integrates-coverage";
  searchPaths = {
    bin = [
      inputs.nixpkgs.findutils
      inputs.nixpkgs.git
    ];
    source = [
      (makePythonPypiEnvironment {
        name = "integrates-coverage";
        sourcesYaml = ./pypi-sources.yaml;
      })
    ];
  };
  entrypoint = projectPath "/integrates/coverage/combine/entrypoint.sh";
}
