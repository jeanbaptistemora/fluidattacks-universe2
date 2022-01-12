{ inputs
, makeScript
, outputs
, ...
}:
makeScript {
  searchPaths = {
    bin = [
      outputs."${inputs.observesIndex.tap.json.bin}"
      outputs."${inputs.observesIndex.tap.mixpanel.bin}"
      outputs."${inputs.observesIndex.target.redshift.bin}"
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
