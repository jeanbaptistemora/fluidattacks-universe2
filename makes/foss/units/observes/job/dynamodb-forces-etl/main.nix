{ makeScript
, outputs
, ...
}:
makeScript {
  searchPaths = {
    bin = [
      outputs."/observes/job/dynamodb-etl"
    ];
  };
  name = "observes-job-dynamodb-forces-etl";
  entrypoint = ./entrypoint.sh;
}
