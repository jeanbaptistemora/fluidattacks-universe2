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
    timeout = 18000;
    vcpus = 4;
  }
