{ inputs
, makeScript
, outputs
, ...
}:
makeScript {
  searchPaths = {
    bin = [
      outputs."/observes/singer/tap-zoho-crm/bin"
      outputs."${inputs.observesIndex.tap.csv.bin}"
      outputs."${inputs.observesIndex.tap.json.bin}"
      outputs."/observes/bin/target-redshift"
      outputs."/observes/service/job-last-success/bin"
    ];
  };
  name = "observes-etl-zoho-crm";
  entrypoint = ./entrypoint.sh;
}
