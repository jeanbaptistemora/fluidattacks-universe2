{ makeScript
, inputs
, ...
}:
makeScript {
  searchPaths = {
    bin = [
      inputs.product.observes-tap-json
      inputs.product.observes-bin-tap-mixpanel
      inputs.product.observes-target-redshift
      inputs.product.observes-bin-service-job-last-success
    ];
    source = [
      (inputs.legacy.importUtility "aws")
      (inputs.legacy.importUtility "sops")
    ];
  };
  name = "observes-scheduled-job-mixpanel-integrates-etl";
  entrypoint = ./entrypoint.sh;
}
