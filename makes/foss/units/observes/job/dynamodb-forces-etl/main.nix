{ makeScript
, inputs
, ...
}:
makeScript {
  replace = { };
  searchPaths = {
    bin = [
      inputs.product.observes-job-dynamodb-etl
    ];
  };
  name = "observes-job-dynamodb-forces-etl";
  entrypoint = ./entrypoint.sh;
}
