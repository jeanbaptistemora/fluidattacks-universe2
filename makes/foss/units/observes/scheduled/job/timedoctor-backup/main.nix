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
      outputs."/observes/bin/tap-timedoctor"
      inputs.product.observes-bin-tap-timedoctor
      outputs."/observes/bin/service/job-last-success"
    ];
    source = [
      (inputs.legacy.importUtility "aws")
      (inputs.legacy.importUtility "gitlab")
      (inputs.legacy.importUtility "sops")
    ];
  };
  name = "observes-scheduled-job-timedoctor-backup";
  entrypoint = ./entrypoint.sh;
}
