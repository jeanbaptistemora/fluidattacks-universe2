{ computeOnAws
, ...
}:
computeOnAws {
  attempts = 5;
  command = [ "./m" "observes.job.gitlab-etl.services" ];
  jobname = "gitlab-etl-services";
  jobqueue = "observes_later";
  name = "observes-scheduled-on-aws-gitlab-etl-services";
  product = "observes";
  secrets = [
    "PRODUCT_API_TOKEN"
    "SERVICES_API_TOKEN"
  ];
  timeout = 7200;
  vcpus = 1;
}
