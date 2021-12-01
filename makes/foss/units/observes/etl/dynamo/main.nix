{ makeScript
, outputs
, ...
}:
makeScript {
  searchPaths = {
    bin = [
      outputs."/observes/service/job-last-success/bin"
      outputs."/observes/singer/tap-dynamo/bin"
      outputs."/observes/singer/tap-json/bin"
      outputs."/observes/bin/target-redshift"
    ];
    source = [
      outputs."/utils/aws"
      outputs."/utils/sops"
    ];
  };
  name = "observes-etl-dynamo";
  entrypoint = ./entrypoint.sh;
}
