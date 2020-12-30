attrs @ {
  skimsPkgs,
  ...
}:

let
  computeOnAws = import ../../../makes/utils/bash-lib/compute-on-aws skimsPkgs;
in
  computeOnAws {
    attempts = 1;
    command = ["./make" "skims-benchmark"];
    jobname = "skims-benchmark";
    jobqueue = "default-uninterruptible";
    name = "skims-benchmark-on-aws";
    product = "skims";
    secrets = [
      "OBSERVES_PROD_AWS_ACCESS_KEY_ID"
      "OBSERVES_PROD_AWS_SECRET_ACCESS_KEY"
      "SKIMS_PROD_AWS_ACCESS_KEY_ID"
      "SKIMS_PROD_AWS_SECRET_ACCESS_KEY"
    ];
    timeout = 18000;
    vcpus = 4;
  }
