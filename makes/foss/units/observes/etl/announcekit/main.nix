{ makeScript
, outputs
, ...
}:
makeScript {
  searchPaths = {
    bin = [
      outputs."/observes/singer/tap-announcekit/bin"
      outputs."/observes/singer/tap-json/bin"
      outputs."/observes/bin/target-redshift"
      outputs."/observes/service/job-last-success/bin"
    ];
    source = [
      (outputs."/utils/aws")
      (outputs."/utils/sops")
    ];
  };
  name = "observes-etl-announcekit";
  entrypoint = ./entrypoint.sh;
}
