{
  inputs,
  makeScript,
  outputs,
  ...
}:
makeScript {
  searchPaths = {
    bin = [
      outputs."/observes/service/job-last-success/bin"
      outputs."${inputs.observesIndex.tap.dynamo.bin}"
      outputs."${inputs.observesIndex.tap.json.bin}"
      outputs."${inputs.observesIndex.target.redshift.bin}"
    ];
    source = [
      outputs."/utils/aws"
      outputs."/observes/common/db-creds"
    ];
  };
  name = "observes-etl-dynamo-v2";
  entrypoint = ./entrypoint.sh;
}
