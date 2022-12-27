{gitlabCi, ...}: let
  gitlabBranchNotTrunk = gitlabCi.rules.branchNot "trunk";
  gitlabBranchTrunk = gitlabCi.rules.branch "trunk";

  gitlabTitleMatchingMakes = gitlabCi.rules.titleMatching "^(all|forces)";

  gitlabOnlyProd = [
    gitlabBranchTrunk
    gitlabCi.rules.notSchedules
    gitlabCi.rules.notTriggers
    gitlabTitleMatchingMakes
  ];
  gitlabOnlyDev = [
    gitlabBranchNotTrunk
    gitlabCi.rules.notMrs
    gitlabCi.rules.notSchedules
    gitlabCi.rules.notTriggers
    gitlabTitleMatchingMakes
  ];

  gitlabDeployApp = {
    rules = gitlabOnlyProd;
    stage = "deploy-app";
    tags = ["small"];
  };
  gitlabDeployAppDev = {
    rules = gitlabOnlyDev;
    stage = "build";
    tags = ["small"];
  };
  gitlabLint = {
    rules = gitlabOnlyDev;
    stage = "lint-code";
    tags = ["small"];
  };
in {
  pipelines = {
    forces = {
      gitlabPath = "/forces/gitlab-ci.yaml";
      jobs = [
        {
          output = "/deployContainerImage/forcesDev";
          gitlabExtra = gitlabDeployAppDev;
        }
        {
          output = "/deployContainerImage/forcesProd";
          gitlabExtra = gitlabDeployApp;
        }
        {
          output = "/lintPython/module/forces";
          gitlabExtra = gitlabLint;
        }
        {
          output = "/lintPython/module/forcesTests";
          gitlabExtra = gitlabLint;
        }
        {
          output = "/pipelineOnGitlab/forces";
          gitlabExtra = gitlabLint;
        }
      ];
    };
  };
}
