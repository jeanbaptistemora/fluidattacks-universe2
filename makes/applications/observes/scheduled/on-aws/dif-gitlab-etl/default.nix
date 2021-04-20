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
    "AUTONOMIC_API_TOKEN"
    "SERVICES_API_TOKEN"
    "PRODUCT_API_TOKEN"
  ];
  timeout = 14400;
  vcpus = 1;
}
