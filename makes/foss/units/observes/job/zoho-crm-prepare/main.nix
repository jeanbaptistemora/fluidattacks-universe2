{ makeScript
, inputs
, ...
}:
makeScript {
  searchPaths = {
    bin = [
      inputs.product.observes-bin-streamer-zoho-crm
      inputs.product.observes-bin-service.job-last-success
    ];
  };
  name = "observes-job-zoho-crm-prepare";
  entrypoint = ./entrypoint.sh;
}
