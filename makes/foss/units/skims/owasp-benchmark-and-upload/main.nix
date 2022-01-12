{ inputs
, makeScript
, outputs
, ...
}:
makeScript {
  name = "skims-owasp-benchmark-and-upload";
  searchPaths = {
    bin = [
      outputs."/skims/owasp-benchmark"
      outputs."${inputs.observesIndex.tap.json.bin}"
      outputs."${inputs.observesIndex.target.redshift.bin}"
    ];
    source = [
      outputs."/utils/aws"
      outputs."/utils/sops"
    ];
  };
  entrypoint = ./entrypoint.sh;
}
