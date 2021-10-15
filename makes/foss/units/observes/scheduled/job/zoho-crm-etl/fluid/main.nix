{ makeScript
, inputs
, outputs
, ...
}:
makeScript {
  searchPaths = {
    bin = [ outputs."/observes/job/zoho-crm-etl" ];
    source = [
      (inputs.legacy.importUtility "aws")
      (inputs.legacy.importUtility "sops")
    ];
  };
  name = "observes-scheduled-job-zoho-crm-etl-fluid";
  entrypoint = ./entrypoint.sh;
}
