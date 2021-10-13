{ makeScript
, inputs
, projectPath
, ...
}:
makeScript {
  searchPaths = {
    bin = [
      inputs.product.observes-bin-code-etl
    ];
    source = [
      (inputs.legacy.importUtility "aws")
      (inputs.legacy.importUtility "git")
      (inputs.legacy.importUtility "sops")
    ];
  };
  name = "observes-scheduled-job-code-etl-amend";
  entrypoint = projectPath "/makes/foss/units/observes/scheduled/job/code-etl-amend/entrypoint.sh";
}
