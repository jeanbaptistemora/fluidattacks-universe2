{
  inputs,
  makeScript,
  outputs,
  ...
}:
makeScript {
  searchPaths = {
    bin = [
      outputs."${inputs.observesIndex.tap.dynamo.bin}"
      outputs."${inputs.observesIndex.tap.json.bin}"
    ];
    source = [
      outputs."${inputs.observesIndex.target.redshift_2.bin}"
      outputs."${inputs.observesIndex.service.job_last_success.bin}"
      outputs."/common/utils/aws"
    ];
  };
  name = "observes-etl-dynamo-v3";
  entrypoint = ./entrypoint.sh;
}
