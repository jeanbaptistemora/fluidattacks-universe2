{ makeScript
, outputs
, inputs
, ...
}:
makeScript {
  searchPaths = {
    bin = [
      outputs."/observes/bin/tap-delighted"
      outputs."/observes/bin/tap-json"
      inputs.product.observes-target-redshift
      outputs."/observes/bin/service/job-last-success"
    ];
    source = [
      (inputs.legacy.importUtility "aws")
      (inputs.legacy.importUtility "sops")
    ];
  };
  name = "observes-job-delighted-etl";
  entrypoint = ./entrypoint.sh;
}
