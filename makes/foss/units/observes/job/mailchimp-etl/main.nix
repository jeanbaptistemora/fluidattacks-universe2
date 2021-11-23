{ makeScript
, outputs
, ...
}:
makeScript {
  searchPaths = {
    bin = [
      outputs."/observes/bin/target-redshift"
      outputs."/observes/singer/tap-json/bin"
      outputs."/observes/singer/tap-mailchimp/bin"
      outputs."/observes/bin/service/job-last-success"
    ];
    source = [
      outputs."/utils/aws"
      outputs."/utils/sops"
    ];
  };
  name = "observes-job-mailchimp-etl";
  entrypoint = ./entrypoint.sh;
}
