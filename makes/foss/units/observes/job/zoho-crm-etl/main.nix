{ makeScript
, outputs
, ...
}:
makeScript {
  searchPaths = {
    bin = [
      outputs."/observes/bin/streamer-zoho-crm"
      outputs."/observes/bin/tap-csv"
      outputs."/observes/bin/tap-json"
      outputs."/observes/bin/target-redshift"
      outputs."/observes/bin/service/job-last-success"
    ];
  };
  name = "observes-job-zoho-crm-etl";
  entrypoint = ./entrypoint.sh;
}
