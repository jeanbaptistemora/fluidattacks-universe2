{ computeOnAws
, ...
}:
computeOnAws {
  attempts = 5;
  command = [ "./m" "observes.job.checkly-etl" ];
  jobname = "checkly-etl";
  jobqueue = "observes_later";
  name = "observes-scheduled-on-aws-checkly-etl";
  product = "observes";
  secrets = [
    "PRODUCT_API_TOKEN"
  ];
  timeout = 3600;
  vcpus = 1;
}
