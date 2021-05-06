{ computeOnAws
, ...
}:
computeOnAws {
  attempts = 5;
  command = [ "./m" "observes.job.bugsnag-etl" ];
  jobname = "bugsnag-etl";
  jobqueue = "observes_later";
  name = "observes-scheduled-on-aws-bugsnag-etl";
  product = "observes";
  secrets = [
    "PRODUCT_API_TOKEN"
  ];
  timeout = 3600;
  vcpus = 1;
}
