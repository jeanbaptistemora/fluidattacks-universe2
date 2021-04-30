{ computeOnAws
, makeEntrypoint
, path
, ...
}:
let
  uploadGroup = computeOnAws {
    attempts = 5;
    command = [ "./m" "observes.scheduled.job.code-etl-upload" ];
    jobname = "code-etl-upload";
    jobqueue = "observes_later";
    name = "aws-batch-code-etl-upload";
    product = "observes";
    secrets = [
      "INTEGRATES_API_TOKEN"
      "PRODUCT_API_TOKEN"
      "SERVICES_API_TOKEN"
    ];
    timeout = 7200;
    vcpus = 1;
  };
in
makeEntrypoint {
  searchPaths = {
    envPaths = [
      uploadGroup
    ];
    envUtils = [
      "/makes/utils/aws"
      "/makes/utils/git"
      "/makes/utils/sops"
    ];
  };
  name = "observes-scheduled-on-aws-code-etl-upload";
  template = path "/makes/applications/observes/scheduled/on-aws/code-etl-upload/entrypoint.sh";
}
