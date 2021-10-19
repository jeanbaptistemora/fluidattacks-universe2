{ makeScript
, inputs
, outputs
, ...
}:
makeScript {
  searchPaths = {
    bin = [
      inputs.product.observes-target-redshift
      inputs.product.observes-tap-json
      inputs.product.observes-bin-tap-mailchimp
      outputs."/observes/bin/tap-mailchimp"
      outputs."/observes/bin/service/job-last-success"
    ];
    source = [
      (inputs.legacy.importUtility "aws")
      (inputs.legacy.importUtility "sops")
    ];
  };
  name = "observes-job-mailchimp-etl";
  entrypoint = ./entrypoint.sh;
}
