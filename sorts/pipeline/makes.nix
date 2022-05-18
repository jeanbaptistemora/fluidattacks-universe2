{gitlabCi, ...}: let
  gitlabBranchMaster = gitlabCi.rules.branch "master";
  gitlabBranchNotMaster = gitlabCi.rules.branchNot "master";

  gitlabTitleMatchingSorts = gitlabCi.rules.titleMatching "^(all|sorts)";

  gitlabOnlyDev = [
    gitlabBranchNotMaster
    gitlabCi.rules.notMrs
    gitlabCi.rules.notSchedules
    gitlabCi.rules.notTriggers
    gitlabTitleMatchingSorts
  ];
  gitlabOnlyMaster = [
    gitlabBranchMaster
    gitlabCi.rules.notSchedules
    gitlabCi.rules.notTriggers
    gitlabTitleMatchingSorts
  ];

  gitlabDeployInfra = {
    resource_group = "$CI_JOB_NAME";
    rules = gitlabOnlyMaster;
    stage = "deploy-infra";
    tags = ["autoscaling"];
  };
  gitlabLint = {
    rules = gitlabOnlyDev;
    stage = "lint-code";
    tags = ["autoscaling"];
  };
  gitlabTest = {
    rules = gitlabOnlyDev;
    stage = "test-code";
    tags = ["autoscaling"];
  };
  gitlabTestInfra = {
    rules = gitlabOnlyDev;
    stage = "test-infra";
    tags = ["autoscaling"];
  };
in {
  pipelines = {
    sorts = {
      gitlabPath = "/sorts/gitlab-ci.yaml";
      jobs = [
        {
          output = "/deployTerraform/sorts";
          gitlabExtra = gitlabDeployInfra;
        }
        {
          output = "/lintPython/dirOfModules/sorts";
          gitlabExtra = gitlabLint;
        }
        {
          output = "/lintPython/imports/sorts";
          gitlabExtra = gitlabLint;
        }
        {
          output = "/lintPython/module/sortsTests";
          gitlabExtra = gitlabLint;
        }
        {
          output = "/lintPython/module/sortsTraining";
          gitlabExtra = gitlabLint;
        }
        {
          output = "/lintTerraform/sorts";
          gitlabExtra = gitlabLint;
        }
        {
          output = "/sorts/association-rules/check/types";
          gitlabExtra = gitlabLint;
        }
        {
          output = "/sorts/extract-features";
          gitlabExtra = {
            interruptible = false;
            parallel = 15;
            rules = [
              (gitlabCi.rules.schedules)
              (gitlabCi.rules.varIsDefined "sorts_extract_features")
              (gitlabCi.rules.always)
            ];
            stage = "pre-build";
            tags = ["autoscaling-large"];
          };
        }
        {
          output = "/sorts/merge-features";
          gitlabExtra = {
            interruptible = false;
            needs = ["/sorts/extract-features"];
            parallel = 15;
            rules = [
              (gitlabCi.rules.schedules)
              (gitlabCi.rules.varIsDefined "sorts_extract_features")
              (gitlabCi.rules.always)
            ];
            stage = "build";
            tags = ["autoscaling"];
          };
        }
        {
          output = "/testPython/sorts";
          gitlabExtra = gitlabTest;
        }
        {
          output = "/testTerraform/sorts";
          gitlabExtra = gitlabTestInfra;
        }
      ];
    };
  };
}
