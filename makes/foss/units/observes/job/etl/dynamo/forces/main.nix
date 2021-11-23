{ makeScript
, outputs
, ...
}:
makeScript {
  searchPaths = {
    bin = [
      outputs."/observes/etl/dynamodb"
    ];
  };
  name = "observes-job-etl-dynamo-forces";
  entrypoint = ./entrypoint.sh;
}
