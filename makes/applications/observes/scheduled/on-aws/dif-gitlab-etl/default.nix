{ computeOnAws
, ...
}:
computeOnAws {
  attempts = 5;
  command = [ "./m" "observes.scheduled.job.dif-gitlab-etl" ];
  jobname = "dif-gitlab-etl";
  jobqueue = "spot_later";
  name = "observes-scheduled-on-aws-dif-gitlab-etl";
  product = "observes";
  secrets = [
    "GITLAB_API_USER"
    "GITLAB_API_TOKEN"
    "OBSERVES_PROD_AWS_ACCESS_KEY_ID"
    "OBSERVES_PROD_AWS_SECRET_ACCESS_KEY"
  ];
  timeout = 14400;
  vcpus = 1;
}
