{ path
, observesPkgs
, ...
} @ _:
let
  computeOnAws = import (path "/makes/utils/compute-on-aws") path observesPkgs;
  uploadGroup = computeOnAws {
    attempts = 5;
    command = [ "./make" "observes/code-etl-upload" ];
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
  makeEntrypoint = import (path "/makes/utils/make-entrypoint") path observesPkgs;
in
makeEntrypoint {
  arguments = {
    envUploadGroupBin = "${uploadGroup}/bin";
    envUtilsBashLibAws = import (path "/makes/utils/aws") path observesPkgs;
    envUtilsBashLibGit = import (path "/makes/utils/use-git-repo") path observesPkgs;
    envUtilsBashLibSops = import (path "/makes/utils/sops") path observesPkgs;
  };
  name = "observes-scheduled-code-etl-upload";
  template = path "/makes/applications/observes/scheduled-code-etl-upload/entrypoint.sh";
}
