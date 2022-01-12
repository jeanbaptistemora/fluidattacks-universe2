{ inputs
, makeScript
, outputs
, ...
}:
makeScript {
  searchPaths = {
    bin = [
      outputs."/observes/bin/target-redshift"
      outputs."${inputs.observesIndex.tap.json.bin}"
      outputs."/observes/singer/tap-mailchimp/bin"
      outputs."/observes/service/job-last-success/bin"
    ];
    source = [
      outputs."/utils/aws"
      outputs."/utils/sops"
    ];
  };
  name = "observes-etl-mailchimp";
  entrypoint = ./entrypoint.sh;
}
