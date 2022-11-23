{
  inputs,
  makeScript,
  outputs,
  projectPath,
  ...
}:
makeScript {
  name = "integrates-web-forces";
  replace = {
    __argIntegratesSecrets__ = projectPath "/integrates";
  };
  searchPaths = {
    bin = [
      inputs.nixpkgs.coreutils
      inputs.nixpkgs.kubectl
      outputs."/forces"
    ];
    source = [
      outputs."/common/utils/aws"
      outputs."/common/utils/sops"
    ];
  };
  entrypoint = ./entrypoint.sh;
}
