{
  inputs,
  makeScript,
  outputs,
  projectPath,
  ...
}:
makeScript {
  replace = {
    __argSecretsDev__ = projectPath "/skims/secrets/dev.yaml";
    __argSecretsProd__ = projectPath "/skims/secrets/prod.yaml";
  };
  name = "skims-sca-patch";
  searchPaths = {
    bin = [
      inputs.nixpkgs.python38
      outputs."/skims"
    ];
    source = [
      outputs."/common/utils/aws"
      outputs."/common/utils/sops"
      outputs."/skims/config/runtime"
    ];
  };
  entrypoint = ./entrypoint.sh;
}
