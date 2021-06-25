{ computeOnAws
, ...
}:
computeOnAws {
  attempts = 2;
  command = [ "./m" "integrates.subscriptions.user-to-entity" ];
  jobname = "integrates-subscriptions-user-to-entity";
  jobqueue = "dedicated_later";
  name = "integrates-subscriptions-user-to-entity-on-aws";
  product = "integrates";
  secrets = [
    "PRODUCT_API_TOKEN"
  ];
  timeout = 7200;
  vcpus = 4;
}
