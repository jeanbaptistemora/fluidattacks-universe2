{ gitlabCi
, ...
}:
let
  gitlabBranchNotMaster = gitlabCi.rules.branchNot "master";

  gitlabTitleMatchingMelts = gitlabCi.rules.titleMatching "^(all|melts)";

  gitlabOnlyDev = [
    gitlabBranchNotMaster
    gitlabCi.rules.notMrs
    gitlabCi.rules.notSchedules
    gitlabCi.rules.notTriggers
    gitlabTitleMatchingMelts
  ];

  gitlabLint = {
    rules = gitlabOnlyDev;
    stage = "lint-code";
    tags = [ "autoscaling" ];
  };
in
{
  pipelines = {
    melts = {
      gitlabPath = "/makes/melts/gitlab-ci.yaml";
      jobs = [
        {
          output = "/lintPython/module/melts";
          gitlabExtra = gitlabLint;
        }
      ];
    };
  };
}
