{
  inputs,
  makeScript,
  outputs,
  ...
}:
makeScript {
  name = "skims-benchmark-owasp-upload";
  searchPaths = {
    bin = [
      outputs."/skims/benchmark/owasp"
      outputs."${inputs.observesIndex.tap.json.bin}"
    ];
    source = [
      outputs."${inputs.observesIndex.target.redshift.bin}"
      outputs."/common/utils/aws"
      outputs."/observes/common/db-creds"
    ];
  };
  entrypoint = ./entrypoint.sh;
}
