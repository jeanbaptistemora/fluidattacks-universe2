{ computeOnAws
, ...
}:
computeOnAws {
  attempts = 3;
  command = [ "./m" "integrates.subscriptions.user-to-entity" ];
  jobname = "integrates-subscriptions-user-to-entity";
  jobqueue = "dedicated_later";
  name = "integrates-subscriptions-user-to-entity-on-aws";
  product = "integrates";
  secrets = [
    "PRODUCT_API_TOKEN"
  ];
  timeout = 14400;
  vcpus = 2;
}
