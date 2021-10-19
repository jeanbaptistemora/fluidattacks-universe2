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
      outputs."/observes/bin/tap-json"
      outputs."/observes/bin/target-redshift"
    ];
    source = [
      (inputs.legacy.importUtility "aws")
      (inputs.legacy.importUtility "sops")
    ];
  };
  entrypoint = ./entrypoint.sh;
}
