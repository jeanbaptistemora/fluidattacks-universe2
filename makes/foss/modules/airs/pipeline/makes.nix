{ gitlabCi
, ...
}:
let
  gitlabBranchNotMaster = gitlabCi.rules.branchNot "master";
  gitlabBranchMaster = gitlabCi.rules.branch "master";

  gitlabTitleMatchingAirs = gitlabCi.rules.titleMatching "^(all|airs)";

  gitlabOnlyMaster = [
    gitlabBranchMaster
    gitlabCi.rules.notSchedules
    gitlabCi.rules.notTriggers
    gitlabTitleMatchingAirs
  ];
  gitlabOnlyDev = [
    gitlabBranchNotMaster
    gitlabCi.rules.notMrs
    gitlabCi.rules.notSchedules
    gitlabCi.rules.notTriggers
    gitlabTitleMatchingAirs
  ];
  gitlabLintJob = {
    rules = gitlabOnlyDev;
    stage = "lint-code";
    tags = [ "autoscaling" ];
  };
in
{
  pipelines = {
    airs = {
      gitlabPath = "/makes/foss/modules/airs/gitlab-ci.yaml";
      jobs = [
        {
          output = "/airs/eph";
          gitlabExtra = {
            rules = gitlabOnlyDev;
            stage = "deploy-app";
            tags = [ "autoscaling" ];
          };
        }
        {
          output = "/airs/prod";
          gitlabExtra = {
            rules = gitlabOnlyMaster;
            stage = "deploy-app";
            tags = [ "autoscaling" ];
          };
        }
        {
          output = "/airs/lint/code";
          gitlabExtra = gitlabLintJob;
        }
        {
          output = "/airs/lint/content";
          gitlabExtra = gitlabLintJob;
        }
        {
          output = "/airs/lint/styles";
          gitlabExtra = gitlabLintJob;
        }
      ];
    };
  };
}
