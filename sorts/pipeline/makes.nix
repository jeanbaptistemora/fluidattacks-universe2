{gitlabCi, ...}: let
  gitlabBranchTrunk = gitlabCi.rules.branch "trunk";
  gitlabBranchNotTrunk = gitlabCi.rules.branchNot "trunk";

  gitlabTitleMatchingSorts = gitlabCi.rules.titleMatching "^(all|sorts)";

  gitlabOnlyDev = [
    gitlabBranchNotTrunk
    gitlabCi.rules.notMrs
    gitlabCi.rules.notSchedules
    gitlabCi.rules.notTriggers
    gitlabTitleMatchingSorts
  ];
  gitlabOnlyProd = [
    gitlabBranchTrunk
    gitlabCi.rules.notSchedules
    gitlabCi.rules.notTriggers
    gitlabTitleMatchingSorts
  ];

  gitlabDeployInfra = {
    resource_group = "$CI_JOB_NAME";
    rules = gitlabOnlyProd;
    stage = "deploy-infra";
    tags = ["small"];
  };
  gitlabLint = {
    rules = gitlabOnlyDev;
    stage = "lint-code";
    tags = ["small"];
  };
  gitlabTest = {
    rules = gitlabOnlyDev;
    stage = "test-code";
    tags = ["small"];
  };
  gitlabTestInfra = {
    rules = gitlabOnlyDev;
    stage = "test-infra";
    tags = ["small"];
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
            tags = ["large"];
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
            tags = ["large"];
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
