{ makeScript
, outputs
, inputs
, ...
}:
makeScript {
  searchPaths = {
    bin = [
      outputs."/observes/bin/service/job-last-success"
      outputs."/observes/bin/tap-bugsnag"
      outputs."/observes/bin/tap-json"
      outputs."/observes/bin/target-redshift"
    ];
    source = [
      (inputs.legacy.importUtility "aws")
      (inputs.legacy.importUtility "sops")
    ];
  };
  name = "observes-job-bugsnag-etl";
  entrypoint = ./entrypoint.sh;
}
