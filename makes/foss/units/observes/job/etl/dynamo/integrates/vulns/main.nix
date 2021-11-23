{ makeScript
, outputs
, ...
}:
makeScript {
  searchPaths.bin = [ outputs."/observes/etl/dynamodb/table" ];
  name = "observes-job-etl-dynamo-integrates-vulns";
  entrypoint = ./entrypoint.sh;
}
