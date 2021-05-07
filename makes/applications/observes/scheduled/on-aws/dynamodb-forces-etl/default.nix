{ nixpkgs
, path
, ...
}:
let
  computeOnAws = import (path "/makes/utils/compute-on-aws") path nixpkgs;
in
computeOnAws {
  attempts = 5;
  command = [ "./m" "observes.job.dynamodb-forces-etl" ];
  jobname = "dynamodb-forces-etl";
  jobqueue = "observes_later";
  name = "observes-scheduled-on-aws-dynamodb-forces-etl";
  product = "observes";
  secrets = [
    "PRODUCT_API_TOKEN"
  ];
  timeout = 18000;
  vcpus = 2;
}
