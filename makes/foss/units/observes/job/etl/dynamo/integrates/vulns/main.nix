{ makeScript
, outputs
, ...
}:
makeScript {
  searchPaths.bin = [ outputs."/observes/etl/dynamo/table" ];
  name = "observes-job-etl-dynamo-integrates-vulns";
  entrypoint = ./entrypoint.sh;
}
