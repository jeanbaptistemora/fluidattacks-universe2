{
  inputs,
  makeScript,
  outputs,
  ...
}:
makeScript {
  name = "integrates-streams";
  searchPaths = {
    bin = [
      inputs.nixpkgs.python39
    ];
    source = [
      outputs."/common/utils/aws"
      outputs."/common/utils/sops"
    ];
  };
  entrypoint = ./entrypoint.sh;
}
