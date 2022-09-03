{
  inputs,
  makeScript,
  outputs,
  ...
}:
makeScript {
  replace = {
    __argSecretsAwsProd__ = outputs."/secretsForAwsFromGitlab/prodObserves";
  };
  searchPaths = {
    bin = [
      inputs.nixpkgs.awscli
      inputs.nixpkgs.coreutils
      inputs.nixpkgs.jq
      outputs."${inputs.observesIndex.tap.timedoctor.bin}"
    ];
    source = [
      outputs."${inputs.observesIndex.service.job_last_success.bin}"
      outputs."/common/utils/gitlab"
      outputs."/common/utils/sops"
      outputs."/observes/common/db-creds"
    ];
  };
  name = "observes-etl-timedoctor-backup";
  entrypoint = ./entrypoint.sh;
}
