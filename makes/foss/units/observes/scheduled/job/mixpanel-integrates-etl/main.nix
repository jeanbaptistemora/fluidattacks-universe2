{ makeScript
, inputs
, outputs
, ...
}:
makeScript {
  searchPaths = {
    bin = [
      outputs."/observes/bin/tap-json"
      outputs."/observes/bin/tap-mixpanel"
      outputs."/observes/bin/target-redshift"
      outputs."/observes/bin/service/job-last-success"
    ];
    source = [
      (outputs."/utils/aws")
      (inputs.legacy.importUtility "sops")
    ];
  };
  name = "observes-scheduled-job-mixpanel-integrates-etl";
  entrypoint = ./entrypoint.sh;
}
