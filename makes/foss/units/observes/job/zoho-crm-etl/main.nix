{ makeScript
, inputs
, outputs
, ...
}:
makeScript {
  searchPaths = {
    bin = [
      inputs.product.observes-bin-streamer-zoho-crm
      inputs.product.observes-bin-tap-csv
      inputs.product.observes-tap-json
      inputs.product.observes-target-redshift
      outputs."/observes/bin/service/job-last-success"
    ];
  };
  name = "observes-job-zoho-crm-etl";
  entrypoint = ./entrypoint.sh;
}
