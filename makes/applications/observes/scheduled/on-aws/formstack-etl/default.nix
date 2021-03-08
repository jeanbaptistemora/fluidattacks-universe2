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
    "OBSERVES_PROD_AWS_ACCESS_KEY_ID"
    "OBSERVES_PROD_AWS_SECRET_ACCESS_KEY"
  ];
  timeout = 14400;
  vcpus = 2;
}
