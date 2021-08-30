{ gitlabCi
, ...
}:
let
  gitlabBranchNotMaster = gitlabCi.rules.branchNot "master";

  gitlabTitleMatchingObserves = gitlabCi.rules.titleMatching "^(all|observes)";

  gitlabOnlyDev = [
    gitlabBranchNotMaster
    gitlabCi.rules.notMrs
    gitlabCi.rules.notSchedules
    gitlabCi.rules.notTriggers
    gitlabTitleMatchingObserves
  ];

  gitlabLint = {
    rules = gitlabOnlyDev;
    stage = "lint-code";
    tags = [ "autoscaling" ];
  };
in
{
  pipelines = {
    observes = {
      gitlabPath = "/makes/observes/gitlab-ci.yaml";
      jobs = [
        {
          output = "/lintPython/module/observesCodeEtl";
          gitlabExtra = gitlabLint;
        }
        {
          output = "/lintPython/module/observesCodeEtlTests";
          gitlabExtra = gitlabLint;
        }
        {
          output = "/lintPython/module/observesJobLastSuccess";
          gitlabExtra = gitlabLint;
        }
        {
          output = "/lintPython/module/observesJobLastSuccessTests";
          gitlabExtra = gitlabLint;
        }
        {
          output = "/lintPython/module/observesServiceBatchStability";
          gitlabExtra = gitlabLint;
        }
      ];
    };
  };
}
