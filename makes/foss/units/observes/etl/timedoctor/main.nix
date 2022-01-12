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
      outputs."${inputs.observesIndex.tap.timedoctor.bin}"
      outputs."${inputs.observesIndex.target.redshift.bin}"
      outputs."/observes/service/job-last-success/bin"
    ];
    source = [
      outputs."/utils/aws"
      outputs."/utils/gitlab"
      outputs."/utils/sops"
    ];
  };
  name = "observes-etl-timedoctor";
  entrypoint = ./entrypoint.sh;
}
