{ makeScript
, outputs
, ...
}:
makeScript {
  searchPaths = {
    bin = [
      outputs."/observes/singer/tap-gitlab/bin"
      outputs."/observes/singer/tap-json/bin"
      outputs."/observes/bin/target-redshift"
    ];
  };
  name = "observes-job-gitlab-etl";
  entrypoint = ./entrypoint.sh;
}
