{ inputs
, makeScript
, outputs
, ...
}:
makeScript {
  entrypoint = "import_and_run jobs_scheduler main";
  searchPaths = {
    source = [
      inputs.product.observes-generic-runner
      outputs."/observes/env/service-jobs-scheduler/runtime"
    ];
  };
  name = "observes-bin-service-jobs-scheduler";
}
