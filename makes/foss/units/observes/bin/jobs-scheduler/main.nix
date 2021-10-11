{ makeScript
, inputs
, ...
}:
makeScript {
  entrypoint = "import_and_run jobs_scheduler main";
  searchPaths = {
    source = [
      inputs.product.observes-generic-runner
      inputs.product.observes-env-service-jobs-scheduler-runtime
    ];
  };
  name = "observes-bin-service-jobs-scheduler";
}
