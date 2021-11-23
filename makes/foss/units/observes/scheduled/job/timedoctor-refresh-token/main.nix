{ makeScript
, outputs
, ...
}:
makeScript {
  searchPaths = {
    bin = [
      outputs."/observes/service/job-last-success/bin"
      outputs."/observes/service/timedoctor-tokens/bin"
    ];
    source = [
      outputs."/utils/aws"
      outputs."/utils/gitlab"
      outputs."/utils/sops"
    ];
  };
  name = "observes-scheduled-job-timedoctor-refresh-token";
  entrypoint = ./entrypoint.sh;
}
