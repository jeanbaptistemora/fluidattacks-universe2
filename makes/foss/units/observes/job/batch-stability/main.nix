{ makeScript
, inputs
, projectPath
, ...
}:
makeScript {
  searchPaths = {
    bin = [
      inputs.product.observes-bin-service-batch-stability
    ];
    source = [
      (inputs.legacy.importUtility "aws")
    ];
  };
  name = "observes-job-batch-stability";
  entrypoint = projectPath "/makes/foss/units/observes/job/batch-stability/entrypoint.sh";
}
