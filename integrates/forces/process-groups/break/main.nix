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
      outputs."/integrates/forces"
    ];
    source = [
      outputs."/common/utils/aws"
      outputs."/common/utils/env"
      outputs."/common/utils/sops"
      outputs."/melts/lib"
    ];
  };
  name = "forces-process-groups-break";
  entrypoint = ./entrypoint.sh;
}
