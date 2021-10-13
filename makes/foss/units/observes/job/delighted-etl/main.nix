{ makeScript
, projectPath
, inputs
, ...
}:
makeScript {
  searchPaths = {
    bin = [
      inputs.product.observes-bin-tap-delighted
      inputs.product.observes-tap-json
      inputs.product.observes-target-redshift
      inputs.product.observes-bin-service-job-last-success
    ];
    source = [
      (inputs.legacy.importUtility "aws")
      (inputs.legacy.importUtility "sops")
    ];
  };
  name = "observes-job-delighted-etl";
  entrypoint = projectPath "/makes/foss/units/observes/job/delighted-etl/entrypoint.sh";
}
