{gitlabCi, ...}: let
  gitlabBranchNotTrunk = gitlabCi.rules.branchNot "trunk";
  gitlabBranchTrunk = gitlabCi.rules.branch "trunk";

  gitlabTitleMatchingAirs = gitlabCi.rules.titleMatching "^(all|airs)";

  gitlabOnlyProd = [
    gitlabBranchTrunk
    gitlabCi.rules.notSchedules
    gitlabCi.rules.notTriggers
    gitlabTitleMatchingAirs
  ];
  gitlabOnlyDev = [
    gitlabBranchNotTrunk
    gitlabCi.rules.notMrs
    gitlabCi.rules.notSchedules
    gitlabCi.rules.notTriggers
    gitlabTitleMatchingAirs
  ];
  gitlabLintJob = {
    rules = gitlabOnlyDev;
    stage = "lint-code";
    tags = ["small"];
  };
in {
  pipelines = {
    airs = {
      gitlabPath = "/airs/gitlab-ci.yaml";
      jobs = [
        {
          output = "/airs/eph";
          gitlabExtra = {
            rules = gitlabOnlyDev;
            stage = "deploy-app";
            tags = ["large"];
          };
        }
        {
          output = "/airs/prod";
          gitlabExtra = {
            rules = gitlabOnlyProd;
            stage = "deploy-app";
            tags = ["large"];
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
        {
          output = "/lintMarkdown/airs";
          gitlabExtra = gitlabLintJob;
        }
        {
          output = "/deployTerraform/airsInfra";
          gitlabExtra = {
            resource_group = "$CI_JOB_NAME";
            rules = gitlabOnlyProd;
            stage = "deploy-infra";
            tags = ["small"];
          };
        }
        {
          output = "/lintTerraform/airsInfra";
          gitlabExtra = gitlabLintJob;
        }
        {
          output = "/testTerraform/airsInfra";
          gitlabExtra = {
            resource_group = "$CI_JOB_NAME";
            rules = gitlabOnlyDev;
            stage = "test-infra";
            tags = ["small"];
          };
        }
      ];
    };
  };
}
