{ makeScript
, inputs
, outputs
, ...
}:
makeScript {
  searchPaths = {
    bin = [
      outputs."/observes/job/dynamodb-etl"
      inputs.nixpkgs.coreutils
      inputs.nixpkgs.jq
    ];
  };
  name = "observes-job-dynamodb-table-etl";
  entrypoint = ./entrypoint.sh;
}
