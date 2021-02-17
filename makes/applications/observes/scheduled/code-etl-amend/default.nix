{ path
, observesPkgs
, ...
} @ _:
let
  computeOnAws = import (path "/makes/utils/compute-on-aws") path observesPkgs;
in
computeOnAws {
  attempts = 5;
  command = [ "./make" "observes.code-etl-amend" ];
  jobname = "code-etl-amend";
  jobqueue = "spot_later";
  name = "observes-scheduled-code-etl-amend";
  product = "observes";
  secrets = [
    "GITLAB_API_TOKEN"
    "GITLAB_API_USER"
    "INTEGRATES_API_TOKEN"
    "OBSERVES_PROD_AWS_ACCESS_KEY_ID"
    "OBSERVES_PROD_AWS_SECRET_ACCESS_KEY"
  ];
  timeout = 18000;
  vcpus = 1;
}
