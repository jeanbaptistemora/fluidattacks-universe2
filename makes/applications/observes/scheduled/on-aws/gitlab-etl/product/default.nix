{ computeOnAws
, ...
}:
computeOnAws {
  attempts = 5;
  command = [ "./m" "observes.job.gitlab-etl.product" ];
  jobname = "gitlab-etl-product";
  jobqueue = "observes_later";
  name = "observes-scheduled-on-aws-gitlab-etl-product";
  product = "observes";
  secrets = [
    "PRODUCT_API_TOKEN"
  ];
  timeout = 7200;
  vcpus = 1;
}
