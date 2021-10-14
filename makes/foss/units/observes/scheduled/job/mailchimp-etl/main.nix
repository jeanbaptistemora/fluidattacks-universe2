{ makeScript
, inputs
, ...
}:
makeScript {
  searchPaths = {
    bin = [
      inputs.product.observes-target-redshift
      inputs.product.observes-tap-json
      inputs.product.observes-bin-tap-mailchimp
      inputs.product.observes-bin-service-job-last-success
    ];
    source = [
      (inputs.legacy.importUtility "aws")
      (inputs.legacy.importUtility "sops")
    ];
  };
  name = "observes-scheduled-job-mailchimp-etl";
  entrypoint = ./entrypoint.sh;
}
