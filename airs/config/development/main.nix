{
  inputs,
  makeScript,
  outputs,
  projectPath,
  ...
}:
makeScript {
  replace = {
    __argAirsSecrets__ = projectPath "/airs/secrets";
    __argAirsNpm__ = outputs."/airs/npm";
  };
  entrypoint = ./entrypoint.sh;
  name = "airs-config-development";
  searchPaths = {
    rpath = [
      inputs.nixpkgs.musl
    ];
    bin = [
      inputs.nixpkgs.utillinux
    ];
    source = [
      outputs."/common/utils/aws"
      outputs."/airs/npm/env"
      outputs."/airs/npm/runtime"
      outputs."/common/utils/sops"
    ];
  };
}
