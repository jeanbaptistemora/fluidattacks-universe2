{ makeScript
, outputs
, ...
}:
makeScript {
  searchPaths = {
    bin = [
      outputs."/observes/bin/streamer-zoho-crm"
      outputs."/observes/bin/service/job-last-success"
    ];
  };
  name = "observes-job-zoho-crm-prepare";
  entrypoint = ./entrypoint.sh;
}
