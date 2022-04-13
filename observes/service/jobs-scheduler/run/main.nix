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
      outputs."/common/utils/aws"
    ];
  };
  name = "observes-service-jobs-scheduler-run";
  entrypoint = ./entrypoint.sh;
}
