{ makeScript
, outputs
, ...
}:
makeScript {
  searchPaths = {
    bin = [
      outputs."/observes/job/gitlab-etl"
    ];
    source = [
      (outputs."/utils/aws")
      (outputs."/utils/sops")
    ];
  };
  name = "observes-job-gitlab-etl-default";
  entrypoint = ./entrypoint.sh;
}
