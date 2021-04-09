{ computeOnAws
, makeEntrypoint
, path
, ...
}:
let
  mirrorGroup = computeOnAws {
    attempts = 5;
    command = [ "./m" "observes.scheduled.job.code-etl-mirror" ];
    jobname = "code-etl-mirror";
    jobqueue = "spot_soon";
    name = "aws-batch-code-etl-mirror";
    product = "observes";
    secrets = [
      "GITLAB_API_TOKEN"
      "GITLAB_API_USER"
      "INTEGRATES_API_TOKEN"
    ];
    timeout = 7200;
    vcpus = 1;
  };
in
makeEntrypoint {
  searchPaths = {
    envPaths = [
      mirrorGroup
    ];
    envUtils = [
      "/makes/utils/aws"
      "/makes/utils/git"
      "/makes/utils/sops"
    ];
  };
  name = "observes-scheduled-on-aws-code-etl-mirror";
  template = path "/makes/applications/observes/scheduled/on-aws/code-etl-mirror/entrypoint.sh";
}
