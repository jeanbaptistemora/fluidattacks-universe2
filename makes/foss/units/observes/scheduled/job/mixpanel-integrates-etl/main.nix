{ makeScript
, outputs
, ...
}:
makeScript {
  searchPaths = {
    bin = [
      outputs."/observes/singer/tap-json/bin"
      outputs."/observes/singer/tap-mixpanel/bin"
      outputs."/observes/bin/target-redshift"
      outputs."/observes/service/job-last-success/bin"
    ];
    source = [
      outputs."/utils/aws"
      outputs."/utils/sops"
    ];
  };
  name = "observes-scheduled-job-mixpanel-integrates-etl";
  entrypoint = ./entrypoint.sh;
}
