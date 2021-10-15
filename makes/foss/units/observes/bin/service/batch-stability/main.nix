{ makeScript
, inputs
, outputs
, ...
}:
makeScript {
  entrypoint = "import_and_run batch_stability.cli main";
  searchPaths = {
    source = [
      outputs."/observes/common/import-and-run"
      inputs.product.observes-generic-runner
      inputs.product.observes-env-service-batch-stability-runtime
    ];
  };
  name = "observes-bin-service-batch-stability";
}
