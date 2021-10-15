{ makeScript
, inputs
, outputs
, ...
}:
makeScript {
  searchPaths = {
    bin = [
      outputs."/observes/bin/streamer-zoho-crm"
      outputs."/observes/bin/tap-csv"
      inputs.product.observes-tap-json
      inputs.product.observes-target-redshift
      outputs."/observes/bin/service/job-last-success"
    ];
  };
  name = "observes-job-zoho-crm-etl";
  entrypoint = ./entrypoint.sh;
}
