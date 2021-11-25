{ makeScript
, outputs
, ...
}:
makeScript {
  searchPaths = {
    bin = [
      outputs."/observes/singer/tap-zoho-crm/bin"
      outputs."/observes/singer/tap-csv/bin"
      outputs."/observes/singer/tap-json/bin"
      outputs."/observes/bin/target-redshift"
      outputs."/observes/service/job-last-success/bin"
    ];
  };
  name = "observes-etl-zoho-crm";
  entrypoint = ./entrypoint.sh;
}
