attrs @ {
  pkgsSkims,
  ...
}:

let
  computeOnAws = import ../../../makes/utils/bash-lib/compute-on-aws pkgsSkims;
in
  computeOnAws {
    attempts = 1;
    command = ["./make" "run" "skims-benchmark"];
    jobname = "skims-benchmark";
    jobqueue = "default-uninterruptible";
    name = "skims-benchmark-on-aws";
    product = "skims";
    secrets = [
      "SKIMS_PROD_AWS_ACCESS_KEY_ID"
      "SKIMS_PROD_AWS_SECRET_ACCESS_KEY"
    ];
    timeout = 18000;
    vcpus = 4;
  }
