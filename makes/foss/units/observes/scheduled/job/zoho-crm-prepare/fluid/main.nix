{ makeScript
, outputs
, ...
}:
makeScript {
  searchPaths = {
    bin = [ outputs."/observes/job/zoho-crm-prepare" ];
    source = [
      (outputs."/utils/aws")
      (outputs."/utils/sops")
    ];
  };
  name = "observes-scheduled-job-zoho-crm-prepare-fluid";
  entrypoint = ./entrypoint.sh;
}
