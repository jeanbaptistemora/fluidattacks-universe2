{
  inputs,
  makeScript,
  outputs,
  ...
}:
makeScript {
  searchPaths = {
    bin = [
      outputs."${inputs.observesIndex.etl.code.bin}"
    ];
    source = [
      outputs."/common/utils/aws"
      outputs."/common/utils/sops"
      outputs."/observes/common/db-creds"
    ];
  };
  name = "observes-etl-code-compute-bills";
  entrypoint = ./entrypoint.sh;
}
