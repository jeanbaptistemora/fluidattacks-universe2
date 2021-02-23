{ path
, skimsPkgs
, ...
}:
let
  computeOnAws = import (path "/makes/utils/compute-on-aws") path skimsPkgs;
in
computeOnAws {
  attempts = 1;
  command = [ "./m" "skims.process-group" ];
  jobname = "skims-process-group";
  jobqueue = "skims_later";
  name = "skims-process-group-on-aws";
  product = "skims";
  secrets = [
    "GITLAB_API_TOKEN"
    "GITLAB_API_USER"
    "INTEGRATES_API_TOKEN"
    "SERVICES_PROD_AWS_ACCESS_KEY_ID"
    "SERVICES_PROD_AWS_SECRET_ACCESS_KEY"
    "SKIMS_PROD_AWS_ACCESS_KEY_ID"
    "SKIMS_PROD_AWS_SECRET_ACCESS_KEY"
  ];
  timeout = 86400;
  vcpus = 4;
}
