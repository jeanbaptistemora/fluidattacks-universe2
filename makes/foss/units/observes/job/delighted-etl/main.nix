{ makeScript
, outputs
, inputs
, ...
}:
makeScript {
  searchPaths = {
    bin = [
      outputs."/observes/bin/tap-delighted"
      outputs."/observes/bin/tap-json"
      outputs."/observes/bin/target-redshift"
      outputs."/observes/bin/service/job-last-success"
    ];
    source = [
      (outputs."/utils/aws")
      (inputs.legacy.importUtility "sops")
    ];
  };
  name = "observes-job-delighted-etl";
  entrypoint = ./entrypoint.sh;
}
