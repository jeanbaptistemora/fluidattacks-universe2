{ makeScript
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
      (outputs."/utils/aws")
      (outputs."/utils/sops")
    ];
  };
  name = "observes-job-mailchimp-etl";
  entrypoint = ./entrypoint.sh;
}
