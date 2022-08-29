{
  inputs,
  makeScript,
  outputs,
  ...
}:
makeScript {
  searchPaths = {
    bin = [
      outputs."${inputs.observesIndex.service.scheduler.bin}"
    ];
    source = [
      outputs."/common/utils/sops"
    ];
  };
  name = "observes-job-scheduler";
  entrypoint = ./entrypoint.sh;
}
