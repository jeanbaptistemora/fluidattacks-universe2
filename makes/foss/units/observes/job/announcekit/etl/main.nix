{ makeScript
, outputs
, inputs
, ...
}:
makeScript {
  searchPaths = {
    bin = [
      inputs.product.observes-bin-tap-announcekit
      inputs.product.observes-tap-json
      inputs.product.observes-target-redshift
      outputs."/observes/bin/service/job-last-success"
    ];
    source = [
      (inputs.legacy.importUtility "aws")
      (inputs.legacy.importUtility "sops")
    ];
  };
  name = "observes-job-announcekit-etl";
  entrypoint = ./entrypoint.sh;
}
