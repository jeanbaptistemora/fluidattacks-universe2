{ inputs
, makeScript
, ...
}:
makeScript {
  searchPaths = {
    bin = [
      inputs.nixpkgs.awscli
      inputs.nixpkgs.coreutils
      inputs.nixpkgs.jq
      inputs.product.observes-bin-tap-timedoctor
      inputs.product.observes-target-redshift
      inputs.product.observes-bin-service-job-last-success
    ];
    source = [
      (inputs.legacy.importUtility "aws")
      (inputs.legacy.importUtility "gitlab")
      (inputs.legacy.importUtility "sops")
    ];
  };
  name = "observes-scheduled-job-timedoctor-etl";
  entrypoint = ./entrypoint.sh;
}
