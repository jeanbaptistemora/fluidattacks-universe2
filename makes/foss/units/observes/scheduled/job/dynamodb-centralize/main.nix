{ makeScript
, outputs
, ...
}:
makeScript {
  searchPaths = {
    bin = [
      outputs."/observes/bin/service/migrate-tables"
    ];
    source = [
      outputs."/utils/aws"
      outputs."/utils/sops"
    ];
  };
  name = "observes-scheduled-job-dynamodb-centralize";
  entrypoint = ./entrypoint.sh;
}
