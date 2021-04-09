{ path
, nixpkgs
, ...
}:
let
  computeOnAws = import (path "/makes/utils/compute-on-aws") path nixpkgs;
in
computeOnAws {
  attempts = 5;
  command = [ "./m" "observes.scheduled.job.code-etl-amend" ];
  jobname = "code-etl-amend";
  jobqueue = "spot_later";
  name = "observes-scheduled-on-aws-code-etl-amend";
  product = "observes";
  secrets = [
    "GITLAB_API_TOKEN"
    "GITLAB_API_USER"
    "INTEGRATES_API_TOKEN"
  ];
  timeout = 18000;
  vcpus = 1;
}
