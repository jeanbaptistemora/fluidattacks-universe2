{ computeOnAws
, ...
}:
computeOnAws {
  attempts = 5;
  command = [ "./m" "observes.job.gitlab-etl.default" ];
  jobname = "gitlab-etl-default";
  jobqueue = "observes_later";
  name = "batch-gitlab-default";
  product = "observes";
  secrets = [
    "AUTONOMIC_API_TOKEN"
  ];
  timeout = 7200;
  vcpus = 1;
}
