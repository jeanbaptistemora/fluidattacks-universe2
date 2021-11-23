{ makeScript
, outputs
, ...
}:
makeScript {
  searchPaths = {
    bin = [
      outputs."/observes/bin/streamer-zoho-crm"
      outputs."/observes/singer/tap-csv/bin"
      outputs."/observes/singer/tap-json/bin"
      outputs."/observes/bin/target-redshift"
      outputs."/observes/service/job-last-success/bin"
    ];
  };
  name = "observes-job-zoho-crm-etl";
  entrypoint = ./entrypoint.sh;
}
