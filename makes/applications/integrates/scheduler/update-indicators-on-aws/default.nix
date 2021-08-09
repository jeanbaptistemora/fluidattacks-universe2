{ computeOnAws
, ...
}:
computeOnAws {
  attempts = 1;
  command = [ "./m" "integrates.scheduler" ];
  jobname = "integrates-scheduler-update-indicators";
  jobqueue = "dedicated_later";
  name = "integrates-scheduler-update-indicators-on-aws";
  product = "integrates";
  secrets = [
    "PRODUCT_API_TOKEN"
  ];
  timeout = 43200;
  vcpus = 4;
}
