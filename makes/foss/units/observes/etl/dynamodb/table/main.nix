{ makeScript
, inputs
, outputs
, ...
}:
makeScript {
  searchPaths = {
    bin = [
      outputs."/observes/etl/dynamodb"
      inputs.nixpkgs.coreutils
      inputs.nixpkgs.jq
    ];
  };
  name = "observes-etl-dynamodb-table";
  entrypoint = ./entrypoint.sh;
}
