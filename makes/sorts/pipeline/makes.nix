{ gitlabCi
, ...
}:
let
  gitlabBranchNotMaster = gitlabCi.rules.branchNot "master";

  gitlabTitleMatchingSorts = gitlabCi.rules.titleMatching "^(all|sorts)";

  gitlabOnlyDev = [
    gitlabBranchNotMaster
    gitlabCi.rules.notMrs
    gitlabCi.rules.notSchedules
    gitlabCi.rules.notTriggers
    gitlabTitleMatchingSorts
  ];

  gitlabLint = {
    rules = gitlabOnlyDev;
    stage = "lint-code";
    tags = [ "autoscaling" ];
  };
in
{
  pipelines = {
    sorts = {
      gitlabPath = "/makes/sorts/gitlab-ci.yaml";
      jobs = [
        {
          output = "/lintPython/dirOfModules/sorts";
          gitlabExtra = gitlabLint;
        }
      ];
    };
  };
}
