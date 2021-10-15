{ makeScript
, inputs
, outputs
, ...
}:
makeScript {
  searchPaths = {
    bin = [
      outputs."/observes/bin/tap-formstack"
      inputs.product.observes-target-redshift
      outputs."/observes/bin/service/job-last-success"
    ];
    source = [
      (inputs.legacy.importUtility "aws")
      (inputs.legacy.importUtility "sops")
    ];
  };
  name = "observes-scheduled-job-formstack-etl";
  entrypoint = ./entrypoint.sh;
}
