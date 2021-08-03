{ gitlabCi
, ...
}:
let
  gitlabBranchNotMaster = gitlabCi.rules.branchNot "master";
  gitlabBranchMaster = gitlabCi.rules.branch "master";

  gitlabTitleMatchingMakes = gitlabCi.rules.titleMatching "^(all|makes)";

  gitlabOnlyMaster = [
    gitlabBranchMaster
    gitlabCi.rules.notSchedules
    gitlabCi.rules.notTriggers
    gitlabTitleMatchingMakes
  ];
  gitlabOnlyDev = [
    gitlabBranchNotMaster
    gitlabCi.rules.notMrs
    gitlabCi.rules.notSchedules
    gitlabCi.rules.notTriggers
    gitlabTitleMatchingMakes
  ];

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
    makes = {
      gitlabPath = "/makes/makes/gitlab-ci.yaml";
      jobs = [
        {
          output = "/deployTerraform/makesCi";
          gitlabExtra = gitlabDeployInfra;
        }
        {
          output = "/deployTerraform/makesCompute";
          gitlabExtra = gitlabDeployInfra;
        }
        {
          output = "/deployTerraform/makesDns";
          gitlabExtra = gitlabDeployInfra;
        }
        {
          output = "/deployTerraform/makesFoss";
          gitlabExtra = gitlabDeployInfra;
        }
        {
          output = "/deployTerraform/makesSecrets";
          gitlabExtra = gitlabDeployInfra;
        }
        {
          output = "/lintTerraform/makesCi";
          gitlabExtra = gitlabLint;
        }
        {
          output = "/lintTerraform/makesCompute";
          gitlabExtra = gitlabLint;
        }
        {
          output = "/lintTerraform/makesDns";
          gitlabExtra = gitlabLint;
        }
        {
          output = "/lintTerraform/makesFoss";
          gitlabExtra = gitlabLint;
        }
        {
          output = "/lintTerraform/makesSecrets";
          gitlabExtra = gitlabLint;
        }
        {
          output = "/lintWithAjv/makes/criteria/compliance";
          gitlabExtra = gitlabLint;
        }
        {
          output = "/lintWithAjv/makes/criteria/requirements";
          gitlabExtra = gitlabLint;
        }
        {
          output = "/lintWithAjv/makes/criteria/vulnerabilities";
          gitlabExtra = gitlabLint;
        }
        {
          output = "/testTerraform/makesCi";
          gitlabExtra = gitlabTestInfra;
        }
        {
          output = "/testTerraform/makesCompute";
          gitlabExtra = gitlabTestInfra;
        }
        {
          output = "/testTerraform/makesCompute";
          gitlabExtra = gitlabTestInfra;
        }
        {
          output = "/testTerraform/makesDns";
          gitlabExtra = gitlabTestInfra;
        }
        {
          output = "/testTerraform/makesFoss";
          gitlabExtra = gitlabTestInfra;
        }
        {
          output = "/testTerraform/makesSecrets";
          gitlabExtra = gitlabTestInfra;
        }
      ];
    };
  };
}
