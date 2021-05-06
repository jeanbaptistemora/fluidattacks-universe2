{ computeOnAws
, ...
}:
computeOnAws {
  attempts = 5;
  command = [ "./m" "observes.job.delighted-etl" ];
  jobname = "delighted-etl";
  jobqueue = "observes_later";
  name = "observes-scheduled-on-aws-delighted-etl";
  product = "observes";
  secrets = [
    "PRODUCT_API_TOKEN"
  ];
  timeout = 3600;
  vcpus = 1;
}
