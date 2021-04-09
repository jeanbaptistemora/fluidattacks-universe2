{ computeOnAws
, ...
}:
computeOnAws {
  attempts = 1;
  command = [ "./m" "skims.process-group" ];
  jobname = "skims-process-group";
  jobqueue = "skims_later";
  name = "skims-process-group-on-aws";
  product = "skims";
  secrets = [
    "GITLAB_API_TOKEN"
  ];
  timeout = 86400;
  vcpus = 2;
}
