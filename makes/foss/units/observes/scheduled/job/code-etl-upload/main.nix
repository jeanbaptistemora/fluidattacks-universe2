{ makeScript
, inputs
, ...
}:
makeScript {
  searchPaths = {
    bin = [
      inputs.product.observes-bin-code-etl
      inputs.product.melts
    ];
    source = [
      (inputs.legacy.importUtility "aws")
      (inputs.legacy.importUtility "git")
      (inputs.legacy.importUtility "sops")
    ];
  };
  name = "observes-scheduled-job-code-etl-upload";
  entrypoint = ./entrypoint.sh;
}
