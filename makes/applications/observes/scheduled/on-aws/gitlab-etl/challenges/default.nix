{ computeOnAws
, ...
}:
computeOnAws {
  attempts = 5;
  command = [ "./m" "observes.job.gitlab-etl.challenges" ];
  jobname = "gitlab-etl-challenges";
  jobqueue = "observes_later";
  name = "observes-scheduled-on-aws-gitlab-etl-challenges";
  product = "observes";
  secrets = [
    "AUTONOMIC_API_TOKEN"
    "PRODUCT_API_TOKEN"
  ];
  timeout = 7200;
  vcpus = 1;
}
