{ makeScript
, outputs
, ...
}:
makeScript {
  searchPaths = {
    bin = [
      outputs."/observes/singer/tap-zoho-crm/bin"
      outputs."/observes/service/job-last-success/bin"
    ];
  };
  name = "observes-etl-zoho-crm-prepare";
  entrypoint = ./entrypoint.sh;
}
