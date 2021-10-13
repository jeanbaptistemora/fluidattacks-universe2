{ makeScript
, inputs
, ...
}:
makeScript {
  searchPaths = {
    bin = [
      inputs.product.observes-bin-tap-formstack
      inputs.product.observes-target-redshift
      inputs.product.observes-bin-service-job-last-success
    ];
    source = [
      (inputs.legacy.importUtility "aws")
      (inputs.legacy.importUtility "sops")
    ];
  };
  name = "observes-scheduled-job-formstack-etl";
  entrypoint = ./entrypoint.sh;
}
