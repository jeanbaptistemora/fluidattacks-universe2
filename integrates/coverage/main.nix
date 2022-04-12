{
  inputs,
  makePythonPypiEnvironment,
  makeScript,
  outputs,
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
      outputs."/utils/aws"
      outputs."/utils/sops"
    ];
  };
  entrypoint = projectPath "/integrates/coverage/entrypoint.sh";
}
