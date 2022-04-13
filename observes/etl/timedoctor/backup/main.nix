{
  inputs,
  makeScript,
  outputs,
  ...
}:
makeScript {
  searchPaths = {
    bin = [
      inputs.nixpkgs.awscli
      inputs.nixpkgs.coreutils
      inputs.nixpkgs.jq
      outputs."${inputs.observesIndex.tap.timedoctor.bin}"
      outputs."/observes/service/job-last-success/bin"
    ];
    source = [
      outputs."/common/utils/aws"
      outputs."/common/utils/gitlab"
      outputs."/common/utils/sops"
      outputs."/observes/common/db-creds"
    ];
  };
  name = "observes-etl-timedoctor-backup";
  entrypoint = ./entrypoint.sh;
}
