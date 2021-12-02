{ makeScript
, inputs
, outputs
, ...
}:
makeScript {
  searchPaths = {
    bin = [
      outputs."/observes/etl/dynamo/v2"
      inputs.nixpkgs.coreutils
      inputs.nixpkgs.jq
    ];
  };
  name = "observes-etl-dynamo-v2-table";
  entrypoint = ./entrypoint.sh;
}
