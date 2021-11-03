{ makeScript
, outputs
, ...
}:
makeScript {
  searchPaths = {
    bin = [
      outputs."/observes/bin/tap-formstack"
      outputs."/observes/bin/target-redshift"
      outputs."/observes/bin/service/job-last-success"
    ];
    source = [
      (outputs."/utils/aws")
      (outputs."/utils/sops")
    ];
  };
  name = "observes-scheduled-job-formstack-etl";
  entrypoint = ./entrypoint.sh;
}
