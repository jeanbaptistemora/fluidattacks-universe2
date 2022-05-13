{
  inputs,
  makeScript,
  outputs,
  ...
}:
makeScript {
  searchPaths = {
    source = [
      outputs."${inputs.observesIndex.service.batch_stability.bin}"
      outputs."/common/utils/aws"
      outputs."/common/utils/sops"
    ];
  };
  name = "observes-job-batch-stability";
  entrypoint = ./entrypoint.sh;
}
