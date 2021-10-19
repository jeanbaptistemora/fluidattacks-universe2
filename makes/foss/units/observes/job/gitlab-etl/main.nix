{ makeScript
, outputs
, ...
}:
makeScript {
  searchPaths = {
    bin = [
      outputs."/observes/bin/tap-gitlab"
      outputs."/observes/bin/tap-json"
      outputs."/observes/bin/target-redshift"
    ];
  };
  name = "observes-job-gitlab-etl";
  entrypoint = ./entrypoint.sh;
}
