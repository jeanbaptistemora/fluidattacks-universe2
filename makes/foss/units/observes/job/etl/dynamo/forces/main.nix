{ makeScript
, outputs
, ...
}:
makeScript {
  searchPaths = {
    bin = [
      outputs."/observes/etl/dynamo"
    ];
  };
  name = "observes-job-etl-dynamo-forces";
  entrypoint = ./entrypoint.sh;
}
