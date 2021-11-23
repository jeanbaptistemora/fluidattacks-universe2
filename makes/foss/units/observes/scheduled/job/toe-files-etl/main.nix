{ makeScript
, outputs
, ...
}:
makeScript {
  searchPaths = {
    bin = [
      outputs."/observes/singer/tap-toe-files/bin"
      outputs."/observes/singer/tap-json/bin"
      outputs."/observes/bin/target-redshift"
    ];
    source = [
      outputs."/utils/aws"
      outputs."/utils/git"
      outputs."/utils/sops"
    ];
  };
  name = "observes-scheduled-job-toe-files-etl";
  entrypoint = ./entrypoint.sh;
}
