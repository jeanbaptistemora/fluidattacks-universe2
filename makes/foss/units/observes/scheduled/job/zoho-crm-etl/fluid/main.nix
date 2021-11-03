{ makeScript
, outputs
, ...
}:
makeScript {
  searchPaths = {
    bin = [ outputs."/observes/job/zoho-crm-etl" ];
    source = [
      (outputs."/utils/aws")
      (outputs."/utils/sops")
    ];
  };
  name = "observes-scheduled-job-zoho-crm-etl-fluid";
  entrypoint = ./entrypoint.sh;
}
