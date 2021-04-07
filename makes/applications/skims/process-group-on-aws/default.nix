{ computeOnAws
, ...
}:
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
    "OBSERVES_PROD_AWS_ACCESS_KEY_ID"
    "OBSERVES_PROD_AWS_SECRET_ACCESS_KEY"
    "SERVICES_PROD_AWS_ACCESS_KEY_ID"
    "SERVICES_PROD_AWS_SECRET_ACCESS_KEY"
    "SKIMS_PROD_AWS_ACCESS_KEY_ID"
    "SKIMS_PROD_AWS_SECRET_ACCESS_KEY"
  ];
  timeout = 86400;
  vcpus = 4;
}
