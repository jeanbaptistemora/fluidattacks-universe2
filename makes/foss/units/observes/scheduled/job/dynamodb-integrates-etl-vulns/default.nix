{ makeScript
, outputs
, ...
}:
makeScript {
  searchPaths.bin = [ outputs."/observes/job/dynamodb-table-etl" ];
  name = "observes-scheduled-job-dynamodb-integrates-etl-vulns";
  entrypoint = ./entrypoint.sh;
}
