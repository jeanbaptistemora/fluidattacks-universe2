{ inputs
, makeScript
, outputs
, ...
}:
makeScript {
  searchPaths = {
    bin = [
      outputs."${inputs.observesIndex.tap.formstack.bin}"
      outputs."${inputs.observesIndex.target.redshift.bin}"
      outputs."/observes/service/job-last-success/bin"
    ];
    source = [
      outputs."/utils/aws"
      outputs."/utils/sops"
    ];
  };
  name = "observes-etl-formstack";
  entrypoint = ./entrypoint.sh;
}
