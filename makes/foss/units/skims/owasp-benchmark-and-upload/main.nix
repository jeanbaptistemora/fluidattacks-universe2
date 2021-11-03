{ makeScript
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
      (outputs."/utils/aws")
      (outputs."/utils/sops")
    ];
  };
  entrypoint = ./entrypoint.sh;
}
