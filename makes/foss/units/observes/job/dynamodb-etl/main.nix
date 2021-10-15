{ makeScript
, inputs
, ...
}:
makeScript {
  searchPaths = {
    bin = [
      inputs.product.observes-bin-service-job-last-success
      inputs.product.observes-bin-streamer-dynamodb
      inputs.product.observes-tap-json
      inputs.product.observes-target-redshift
    ];
    source = [
      (inputs.legacy.importUtility "aws")
      (inputs.legacy.importUtility "sops")
    ];
  };
  name = "observes-job-dynamodb-etl";
  entrypoint = ./entrypoint.sh;
}
