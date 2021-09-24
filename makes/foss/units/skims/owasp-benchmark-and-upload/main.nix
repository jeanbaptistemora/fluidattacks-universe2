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
      inputs.product.observes-tap-json
      inputs.product.observes-target-redshift
    ];
    source = [
      (inputs.legacy.importUtility "aws")
      (inputs.legacy.importUtility "sops")
    ];
  };
  entrypoint = ./entrypoint.sh;
}
