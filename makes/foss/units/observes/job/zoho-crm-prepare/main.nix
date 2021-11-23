{ makeScript
, outputs
, ...
}:
makeScript {
  searchPaths = {
    bin = [
      outputs."/observes/bin/streamer-zoho-crm"
      outputs."/observes/service/job-last-success/bin"
    ];
  };
  name = "observes-job-zoho-crm-prepare";
  entrypoint = ./entrypoint.sh;
}
