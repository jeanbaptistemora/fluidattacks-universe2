{
  makeScript,
  inputs,
  outputs,
  ...
}:
makeScript {
  searchPaths = {
    bin = [
      inputs.nixpkgs.jq
      outputs."/forces"
    ];
    source = [
      outputs."/melts/lib"
      outputs."/common/utils/aws"
      outputs."/common/utils/sops"
    ];
  };
  name = "forces-process-groups-pass";
  entrypoint = ./entrypoint.sh;
}
