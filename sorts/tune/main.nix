{
  makeScript,
  inputs,
  outputs,
  ...
}:
makeScript {
  name = "sorts-tune";
  searchPaths = {
    bin = [inputs.nixpkgs.python38];
    source = [
      outputs."/sorts/config/development"
      outputs."/sorts/config/runtime"
      outputs."/common/utils/sops"
    ];
  };
  entrypoint = ./entrypoint.sh;
}
