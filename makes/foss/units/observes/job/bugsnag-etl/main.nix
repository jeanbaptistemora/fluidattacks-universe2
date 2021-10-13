{ makeScript
, projectPath
, inputs
, ...
}:
makeScript {
  searchPaths = {
    bin = [
      inputs.product.observes-bin-tap-bugsnag
      inputs.product.observes-bin-service-job-last-success
      inputs.product.observes-tap-json
      inputs.product.observes-target-redshift
    ];
    source = [
      (inputs.legacy.importUtility "aws")
      (inputs.legacy.importUtility "sops")
    ];
  };
  name = "observes-job-bugsnag-etl";
  entrypoint = projectPath "/makes/foss/units/observes/job/bugsnag-etl/entrypoint.sh";
}
