{ observesPkgs
, path
, ...
} @ _:
let
  nixPkgs = observesPkgs;
  computeOnAws = import (path "/makes/utils/compute-on-aws") path nixPkgs;
in
computeOnAws {
  attempts = 5;
  command = [ "./make" "observes/job-dif-gitlab-etl" ];
  jobname = "dif-gitlab-etl";
  jobqueue = "spot_later";
  name = "observes-scheduled-dif-gitlab-etl";
  product = "observes";
  secrets = [
    "GITLAB_API_TOKEN"
    "GITLAB_API_USER"
    "OBSERVES_PROD_AWS_ACCESS_KEY_ID"
    "OBSERVES_PROD_AWS_SECRET_ACCESS_KEY"
  ];
  timeout = 14400;
  vcpus = 1;
}
