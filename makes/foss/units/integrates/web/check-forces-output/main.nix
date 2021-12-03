{ inputs
, makeScript
, outputs
, projectPath
, ...
}:
makeScript {
  name = "integrates-web-check-forces-output";
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
      outputs."/utils/aws"
      outputs."/utils/sops"
    ];
  };
  entrypoint = ./entrypoint.sh;
}
