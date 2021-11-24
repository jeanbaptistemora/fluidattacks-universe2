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
  name = "observes-etl-dynamo-forces";
  entrypoint = ./entrypoint.sh;
}
