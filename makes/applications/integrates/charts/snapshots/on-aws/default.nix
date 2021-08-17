{ computeOnAws
, ...
}:
computeOnAws {
  attempts = 1;
  command = [ "./m" "integrates.charts.snapshots" ];
  jobname = "integrates-charts-snapshots";
  jobqueue = "dedicated_later";
  name = "integrates-charts-snapshots-on-aws";
  product = "integrates";
  secrets = [
    "INTEGRATES_API_TOKEN"
    "PRODUCT_API_TOKEN"
  ];
  timeout = 14400;
  vcpus = 4;
}
