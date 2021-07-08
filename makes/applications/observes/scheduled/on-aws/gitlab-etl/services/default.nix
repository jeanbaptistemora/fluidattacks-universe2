{ computeOnAws
, ...
}:
computeOnAws {
  attempts = 5;
  command = [ "./m" "observes.job.gitlab-etl.services" ];
  jobname = "gitlab-etl-services";
  jobqueue = "observes_later";
  name = "batch-gitlab-services";
  product = "observes";
  secrets = [
    "SERVICES_API_TOKEN"
  ];
  timeout = 7200;
  vcpus = 1;
}
