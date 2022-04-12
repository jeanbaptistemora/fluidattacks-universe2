{
  inputs,
  makeScript,
  outputs,
  ...
}:
makeScript {
  searchPaths = {
    bin = [
      outputs."${inputs.observesIndex.tap.zoho_crm.bin}"
      outputs."${inputs.observesIndex.tap.csv.bin}"
      outputs."${inputs.observesIndex.tap.json.bin}"
      outputs."${inputs.observesIndex.target.redshift.bin}"
      outputs."/observes/service/job-last-success/bin"
    ];
  };
  name = "observes-etl-zoho-crm";
  entrypoint = ./entrypoint.sh;
}
