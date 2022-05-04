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
      outputs."/common/utils/sops"
      outputs."${inputs.observesIndex.service.scheduler.bin}"
    ];
  };
  name = "observes-job-scheduler";
  entrypoint = ./entrypoint.sh;
}
