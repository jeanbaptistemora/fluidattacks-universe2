{ makeScript
, outputs
, ...
}:
makeScript {
  searchPaths = {
    bin = [
      outputs."/observes/bin/tap-toe-files"
      outputs."/observes/bin/tap-json"
      outputs."/observes/bin/target-redshift"
    ];
    source = [
      (outputs."/utils/aws")
      (outputs."/utils/git")
      (outputs."/utils/sops")
    ];
  };
  name = "observes-scheduled-job-toe-files-etl";
  entrypoint = ./entrypoint.sh;
}
