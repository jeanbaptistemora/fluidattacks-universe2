{ path, ... } @ attrs:
let
  observes = import (path "/makes/libs/observes") attrs;
in
observes.makeUtils.computeOnAws {
  attempts = 5;
  command = [ "./m" "observes.job.dif-gitlab-etl" ];
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
