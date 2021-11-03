{ makeScript
, outputs
, ...
}:
makeScript {
  searchPaths = {
    bin = [
      outputs."/observes/bin/service/job-last-success"
      outputs."/observes/bin/streamer-dynamodb"
      outputs."/observes/bin/tap-json"
      outputs."/observes/bin/target-redshift"
    ];
    source = [
      (outputs."/utils/aws")
      (outputs."/utils/sops")
    ];
  };
  name = "observes-job-dynamodb-etl";
  entrypoint = ./entrypoint.sh;
}
