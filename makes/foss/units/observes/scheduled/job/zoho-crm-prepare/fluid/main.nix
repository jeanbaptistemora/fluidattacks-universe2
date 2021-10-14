{ inputs
, makeScript
, ...
}:
makeScript {
  searchPaths = {
    bin = [ inputs.product.observes-job-zoho-crm-prepare ];
    source = [
      (inputs.legacy.importUtility "aws")
      (inputs.legacy.importUtility "sops")
    ];
  };
  name = "observes-scheduled-job-zoho-crm-prepare-fluid";
  entrypoint = ./entrypoint.sh;
}
