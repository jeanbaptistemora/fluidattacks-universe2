{ gitlabCi
, ...
}:
let
  gitlabBranchNotMaster = gitlabCi.rules.branchNot "master";
  gitlabBranchMaster = gitlabCi.rules.branch "master";

  gitlabTitleMatchingSkims = gitlabCi.rules.titleMatching "^(all|skims)";

  gitlabOnlyMaster = [
    gitlabBranchMaster
    gitlabCi.rules.notSchedules
    gitlabCi.rules.notTriggers
    gitlabTitleMatchingSkims
  ];
  gitlabOnlyDev = [
    gitlabBranchNotMaster
    gitlabCi.rules.notMrs
    gitlabCi.rules.notSchedules
    gitlabCi.rules.notTriggers
    gitlabTitleMatchingSkims
  ];

  gitlabDeployApp = {
    rules = gitlabOnlyMaster;
    stage = "deploy-app";
    tags = [ "autoscaling" ];
  };
  gitlabDeployInfra = {
    resource_group = "$CI_JOB_NAME";
    rules = gitlabOnlyMaster;
    stage = "deploy-infra";
    tags = [ "autoscaling" ];
  };
  gitlabLint = {
    rules = gitlabOnlyDev;
    stage = "lint-code";
    tags = [ "autoscaling" ];
  };
  gitlabTestInfra = {
    rules = gitlabOnlyDev;
    stage = "test-infra";
    tags = [ "autoscaling" ];
  };
in
{
  pipelines = {
    skims = {
      gitlabPath = "/makes/foss/modules/skims/gitlab-ci.yaml";
      jobs = [
        {
          output = "/deployContainerImage/skimsProd";
          gitlabExtra = gitlabDeployApp;
        }
        {
          output = "/deployTerraform/skims";
          gitlabExtra = gitlabDeployInfra;
        }
        {
          output = "/lintPython/dirOfModules/skims";
          gitlabExtra = gitlabLint;
        }
        {
          output = "/lintPython/imports/skims";
          gitlabExtra = gitlabLint;
        }
        {
          output = "/lintPython/module/skimsTest";
          gitlabExtra = gitlabLint;
        }
        {
          output = "/lintPython/module/skimsTestMocksHttp";
          gitlabExtra = gitlabLint;
        }
        {
          output = "/lintPython/module/skimsTestSdk";
          gitlabExtra = gitlabLint;
        }
        {
          output = "/lintPython/module/skimsProcessGroup";
          gitlabExtra = gitlabLint;
        }
        {
          output = "/lintTerraform/skims";
          gitlabExtra = gitlabLint;
        }
        {
          output = "/testTerraform/skims";
          gitlabExtra = gitlabTestInfra;
        }
        {
          output = "/securePythonWithBandit/skims";
          gitlabExtra = gitlabLint;
        }
      ];
    };
  };
}
