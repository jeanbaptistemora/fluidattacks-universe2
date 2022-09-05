{
  inputs,
  makeScript,
  outputs,
  ...
}:
makeScript {
  searchPaths = {
    source = [
      outputs."/common/utils/aws"
      outputs."${inputs.observesIndex.service.batch_stability.bin}"
      outputs."/common/utils/sops"
    ];
  };
  name = "observes-job-batch-stability";
  entrypoint = ./entrypoint.sh;
}
