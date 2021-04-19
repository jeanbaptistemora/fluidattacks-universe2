{ computeOnAws
, ...
}:
computeOnAws {
  attempts = 1;
  command = [ "./m" "skims.owasp-benchmark-and-upload" ];
  jobname = "skims-benchmark";
  jobqueue = "dedicated_later";
  name = "skims-benchmark-on-aws";
  product = "skims";
  secrets = [
    "PRODUCT_API_TOKEN"
  ];
  timeout = 86400;
  vcpus = 4;
}
