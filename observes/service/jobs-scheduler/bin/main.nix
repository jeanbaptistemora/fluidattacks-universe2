{
  inputs,
  makeScript,
  outputs,
  ...
}:
makeScript {
  entrypoint = ''
    python -c "from jobs_scheduler.cli import main; main()" "$@"
  '';
  searchPaths = {
    source = [
      outputs."${inputs.observesIndex.service.scheduler.env.runtime}"
    ];
  };
  name = "observes-service-jobs-scheduler-bin";
}
