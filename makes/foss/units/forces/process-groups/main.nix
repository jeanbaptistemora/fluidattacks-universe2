{ makeScript
, inputs
, outputs
, ...
}:
makeScript {
  searchPaths = {
    bin = [
      inputs.nixpkgs.jq
      outputs."/forces"
    ];
    source = [
      outputs."/melts/lib"
      outputs."/utils/aws"
      outputs."/utils/sops"
    ];
  };
  name = "forces-process-groups";
  entrypoint = ./entrypoint.sh;
}
