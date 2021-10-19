{ makeScript
, inputs
, outputs
, ...
}:
makeScript {
  searchPaths = {
    bin = [
      outputs."/observes/bin/target-redshift"
      outputs."/observes/bin/tap-json"
      outputs."/observes/bin/tap-mailchimp"
      outputs."/observes/bin/service/job-last-success"
    ];
    source = [
      (inputs.legacy.importUtility "aws")
      (inputs.legacy.importUtility "sops")
    ];
  };
  name = "observes-job-mailchimp-etl";
  entrypoint = ./entrypoint.sh;
}
