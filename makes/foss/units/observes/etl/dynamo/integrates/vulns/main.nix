{ makeScript
, outputs
, ...
}:
makeScript {
  searchPaths.bin = [ outputs."/observes/etl/dynamo/table" ];
  name = "observes-etl-dynamo-integrates-vulns";
  entrypoint = ./entrypoint.sh;
}
