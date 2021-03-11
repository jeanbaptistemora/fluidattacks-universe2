{ path
, nixpkgs
, ...
}:
let
  computeOnAws = import (path "/makes/utils/compute-on-aws") path nixpkgs;
  uploadGroup = computeOnAws {
    attempts = 5;
    command = [ "./m" "observes.scheduled.job.code-etl-upload" ];
    jobname = "code-etl-upload";
    jobqueue = "spot_later";
    name = "aws-batch-code-etl-upload";
    product = "observes";
    secrets = [
      "GITLAB_API_TOKEN"
      "GITLAB_API_USER"
      "INTEGRATES_API_TOKEN"
      "OBSERVES_PROD_AWS_ACCESS_KEY_ID"
      "OBSERVES_PROD_AWS_SECRET_ACCESS_KEY"
    ];
    timeout = 7200;
    vcpus = 1;
  };
  makeEntrypoint = import (path "/makes/utils/make-entrypoint") path nixpkgs;
in
makeEntrypoint {
  arguments = {
    envUploadGroupBin = "${uploadGroup}/bin";
    envUtilsBashLibAws = import (path "/makes/utils/aws") path nixpkgs;
    envUtilsBashLibGit = import (path "/makes/utils/git") path nixpkgs;
    envUtilsBashLibSops = import (path "/makes/utils/sops") path nixpkgs;
  };
  name = "observes-scheduled-on-aws-code-etl-upload";
  template = path "/makes/applications/observes/scheduled/on-aws/code-etl-upload/entrypoint.sh";
}
