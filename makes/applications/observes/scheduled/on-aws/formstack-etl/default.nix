{ computeOnAws
, ...
}:
computeOnAws {
  attempts = 5;
  command = [ "./m" "observes.scheduled.job.formstack-etl" ];
  jobname = "formstack-etl";
  jobqueue = "spot_later";
  name = "observes-scheduled-on-aws-formstack-etl";
  product = "observes";
  secrets = [
    "PRODUCT_API_TOKEN"
  ];
  timeout = 14400;
  vcpus = 2;
}
