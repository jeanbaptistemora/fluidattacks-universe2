{ makeScript
, projectPath
, inputs
, ...
}:
makeScript {
  searchPaths = {
    bin = [
      inputs.product.observes-job-gitlab-etl
    ];
    source = [
      (inputs.legacy.importUtility "aws")
      (inputs.legacy.importUtility "sops")
    ];
  };
  name = "observes-job-gitlab-etl-challenges";
  entrypoint = projectPath "/makes/foss/units/observes/job/gitlab-etl/challenges/entrypoint.sh";
}
