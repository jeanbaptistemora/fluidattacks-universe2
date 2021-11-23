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
      outputs."/observes/bin/service/job-last-success"
    ];
    source = [
      outputs."/utils/aws"
      outputs."/utils/gitlab"
      outputs."/utils/sops"
    ];
  };
  name = "observes-scheduled-job-timedoctor-backup";
  entrypoint = ./entrypoint.sh;
}
