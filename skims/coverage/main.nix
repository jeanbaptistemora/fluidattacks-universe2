{
  inputs,
  makeScript,
  projectPath,
  outputs,
  ...
}:
makeScript {
  replace = {
    __argSecretsDev__ = projectPath "/skims/secrets/dev.yaml";
  };
  name = "skims-coverage";
  searchPaths = {
    bin = [
      inputs.nixpkgs.python3Packages.coverage
      inputs.nixpkgs.findutils
      inputs.nixpkgs.git
      outputs."/common/utils/codecov"
    ];
    source = [
      outputs."/common/utils/aws"
      outputs."/common/utils/sops"
    ];
  };
  entrypoint = ./entrypoint.sh;
}
