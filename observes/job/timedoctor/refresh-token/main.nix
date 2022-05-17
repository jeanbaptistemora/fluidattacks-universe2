{
  inputs,
  makeScript,
  outputs,
  ...
}:
makeScript {
  searchPaths = {
    bin = [
      outputs."/observes/service/timedoctor-tokens/bin"
    ];
    source = [
      outputs."${inputs.observesIndex.service.job_last_success.bin}"
      outputs."/common/utils/aws"
      outputs."/common/utils/sops"
      outputs."/common/utils/gitlab"
      outputs."/observes/common/db-creds"
    ];
  };
  name = "observes-job-timedoctor-refresh-token";
  entrypoint = ./entrypoint.sh;
}
