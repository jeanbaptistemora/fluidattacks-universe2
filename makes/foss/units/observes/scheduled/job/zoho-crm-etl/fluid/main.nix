{ makeScript
, inputs
, ...
}:
makeScript {
  searchPaths = {
    bin = [
      inputs.product.observes-job-zoho-crm-etl
    ];
    source = [
      (inputs.legacy.importUtility "aws")
      (inputs.legacy.importUtility "sops")
    ];
  };
  name = "observes-scheduled-job-zoho-crm-etl-fluid";
  entrypoint = ./entrypoint.sh;
}
