{ makeScript
, inputs
, ...
}:
makeScript {
  searchPaths = {
    bin = [
      inputs.product.observes-job-dynamodb-etl
      inputs.nixpkgs.coreutils
      inputs.nixpkgs.jq
    ];
  };
  name = "observes-job-dynamodb-table-etl";
  entrypoint = ./entrypoint.sh;
}
