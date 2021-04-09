{ computeOnAws
, ...
}:
computeOnAws {
  attempts = 5;
  command = [ "./m" "observes.job.dif-gitlab-etl" ];
  jobname = "dif-gitlab-etl";
  jobqueue = "spot_later";
  name = "observes-scheduled-dif-gitlab-etl";
  product = "observes";
  secrets = [
    "GITLAB_API_TOKEN"
    "GITLAB_API_USER"
  ];
  timeout = 14400;
  vcpus = 1;
}
