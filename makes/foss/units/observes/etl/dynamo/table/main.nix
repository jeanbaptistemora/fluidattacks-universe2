{ makeScript
, inputs
, outputs
, ...
}:
makeScript {
  searchPaths = {
    bin = [
      outputs."/observes/etl/dynamo"
      inputs.nixpkgs.coreutils
      inputs.nixpkgs.jq
    ];
  };
  name = "observes-etl-dynamo-table";
  entrypoint = ./entrypoint.sh;
}
