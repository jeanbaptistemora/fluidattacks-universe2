{
  inputs,
  makeScript,
  outputs,
  ...
}:
makeScript {
  searchPaths = {
    bin = [
      outputs."${inputs.observesIndex.service.batch_stability.bin}"
    ];
    source = [
      outputs."/common/utils/aws"
      outputs."/common/utils/sops"
    ];
  };
  name = "observes-job-batch-stability";
  entrypoint = ./entrypoint.sh;
}
