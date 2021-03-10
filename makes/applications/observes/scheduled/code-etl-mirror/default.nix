{ path
, nixpkgs
, ...
}:
let
  computeOnAws = import (path "/makes/utils/compute-on-aws") path nixpkgs;
  mirrorGroup = computeOnAws {
    attempts = 5;
    command = [ "./m" "observes.job.code-etl-mirror" ];
    jobname = "code-etl-mirror";
    jobqueue = "spot_soon";
    name = "aws-batch-code-etl-mirror";
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
    envMirrorGroupBin = "${mirrorGroup}/bin";
    envUtilsBashLibAws = import (path "/makes/utils/aws") path nixpkgs;
    envUtilsBashLibGit = import (path "/makes/utils/git") path nixpkgs;
    envUtilsBashLibSops = import (path "/makes/utils/sops") path nixpkgs;
  };
  name = "observes-scheduled-code-etl-mirror";
  template = path "/makes/applications/observes/scheduled/code-etl-mirror/entrypoint.sh";
}
