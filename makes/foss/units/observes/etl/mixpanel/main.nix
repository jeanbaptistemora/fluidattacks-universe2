{ inputs
, makeScript
, outputs
, ...
}:
makeScript {
  searchPaths = {
    bin = [
      outputs."${inputs.observesIndex.tap.json.bin}"
      outputs."/observes/singer/tap-mixpanel/bin"
      outputs."/observes/bin/target-redshift"
      outputs."/observes/service/job-last-success/bin"
    ];
    source = [
      outputs."/utils/aws"
      outputs."/utils/sops"
    ];
  };
  name = "observes-etl-mixpanel";
  entrypoint = ./entrypoint.sh;
}
