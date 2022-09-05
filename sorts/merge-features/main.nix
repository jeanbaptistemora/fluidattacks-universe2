{
  makeScript,
  inputs,
  outputs,
  ...
}:
makeScript {
  name = "sorts-merge-features";
  searchPaths = {
    bin = [inputs.nixpkgs.python38];
    source = [
      outputs."/sorts/config/development"
      outputs."/sorts/config/runtime"
      outputs."/common/utils/aws"
      outputs."/common/utils/sops"
    ];
  };
  entrypoint = ./entrypoint.sh;
}
