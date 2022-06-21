{
  inputs,
  makeScript,
  outputs,
  ...
}:
makeScript {
  searchPaths = {
    bin = [
      outputs."${inputs.observesIndex.tap.json.bin}"
    ];
    source = [
      outputs."${inputs.observesIndex.tap.checkly.bin}"
      outputs."${inputs.observesIndex.service.job_last_success.bin}"
      outputs."${inputs.observesIndex.target.redshift.bin}"
      outputs."/common/utils/aws"
      outputs."/common/utils/sops"
      outputs."/observes/common/db-creds"
    ];
  };
  name = "observes-etl-checkly";
  entrypoint = ./entrypoint.sh;
}
