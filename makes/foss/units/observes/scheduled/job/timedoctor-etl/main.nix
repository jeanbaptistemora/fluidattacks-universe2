{ inputs
, makeScript
, outputs
, ...
}:
makeScript {
  searchPaths = {
    bin = [
      inputs.nixpkgs.awscli
      inputs.nixpkgs.coreutils
      inputs.nixpkgs.jq
      outputs."/observes/singer/tap-timedoctor/bin"
      outputs."/observes/bin/target-redshift"
      outputs."/observes/service/job-last-success/bin"
    ];
    source = [
      outputs."/utils/aws"
      outputs."/utils/gitlab"
      outputs."/utils/sops"
    ];
  };
  name = "observes-scheduled-job-timedoctor-etl";
  entrypoint = ./entrypoint.sh;
}
