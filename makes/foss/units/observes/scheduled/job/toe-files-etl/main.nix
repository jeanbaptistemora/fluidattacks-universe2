{ makeScript
, inputs
, ...
}:
makeScript {
  searchPaths = {
    bin = [
      inputs.product.observes-bin-tap-toe-files
      inputs.product.observes-tap-json
      inputs.product.observes-target-redshift
    ];
    source = [
      (inputs.legacy.importUtility "aws")
      (inputs.legacy.importUtility "git")
      (inputs.legacy.importUtility "sops")
    ];
  };
  name = "observes-scheduled-job-toe-files-etl";
  entrypoint = ./entrypoint.sh;
}
