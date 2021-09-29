{ gitlabCi
, ...
}:
let
  gitlabBranchNotMaster = gitlabCi.rules.branchNot "master";
  gitlabBranchMaster = gitlabCi.rules.branch "master";

  gitlabTitleMatchingMakes = gitlabCi.rules.titleMatching "^(all|integrates)";

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

  gitlabDeployAppDev = {
    rules = gitlabOnlyDev;
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
    integrates = {
      gitlabPath = "/makes/foss/modules/integrates/gitlab-ci.yaml";
      jobs = [
        {
          output = "/deployTerraform/integratesBackups";
          gitlabExtra = gitlabDeployInfra;
        }
        {
          output = "/deployTerraform/integratesCache";
          gitlabExtra = gitlabDeployInfra;
        }
        {
          output = "/deployTerraform/integratesDatabase";
          gitlabExtra = gitlabDeployInfra;
        }
        {
          output = "/deployTerraform/integratesFront";
          gitlabExtra = gitlabDeployInfra;
        }
        {
          output = "/deployTerraform/integratesResources";
          gitlabExtra = gitlabDeployInfra;
        }
        {
          output = "/deployTerraform/integratesSecrets";
          gitlabExtra = gitlabDeployInfra;
        }
        {
          output = "/integrates/back/authz-matrix";
          gitlabExtra = gitlabDeployAppDev;
        }
        {
          output = "/integrates/linters/back/schema";
          gitlabExtra = gitlabLint;
        }
        {
          output = "/integrates/linters/charts";
          gitlabExtra = gitlabLint;
        }
        {
          output = "/lintPython/dirOfModules/integrates";
          gitlabExtra = gitlabLint;
        }
        {
          output = "/lintPython/dirOfModules/integratesBackChartsGenerators";
          gitlabExtra = gitlabLint;
        }
        {
          output = "/lintPython/imports/integrates";
          gitlabExtra = gitlabLint;
        }
        {
          output = "/lintPython/module/integratesBackDeployPermissionsMatrix";
          gitlabExtra = gitlabLint;
        }
        {
          output = "/lintPython/module/integratesBackMigrations";
          gitlabExtra = gitlabLint;
        }
        # TODO: https://gitlab.com/fluidattacks/product/-/issues/5246
        # {
        #   output = "/lintPython/module/integratesBackTests";
        #   gitlabExtra = gitlabLint;
        # }
        {
          output = "/lintPython/module/integratesBackTestsE2e";
          gitlabExtra = gitlabLint;
        }
        {
          output = "/lintTerraform/integratesBackups";
          gitlabExtra = gitlabLint;
        }
        {
          output = "/lintTerraform/integratesCache";
          gitlabExtra = gitlabLint;
        }
        {
          output = "/lintTerraform/integratesDatabase";
          gitlabExtra = gitlabLint;
        }
        {
          output = "/lintTerraform/integratesFront";
          gitlabExtra = gitlabLint;
        }
        {
          output = "/lintTerraform/integratesResources";
          gitlabExtra = gitlabLint;
        }
        {
          output = "/lintTerraform/integratesSecrets";
          gitlabExtra = gitlabLint;
        }
        {
          output = "/pipelineOnGitlab/integrates";
          gitlabExtra = gitlabLint;
        }
        {
          output = "/testTerraform/integratesBackups";
          gitlabExtra = gitlabTestInfra;
        }
        {
          output = "/testTerraform/integratesCache";
          gitlabExtra = gitlabTestInfra;
        }
        {
          output = "/testTerraform/integratesDatabase";
          gitlabExtra = gitlabTestInfra;
        }
        {
          output = "/testTerraform/integratesFront";
          gitlabExtra = gitlabTestInfra;
        }
        {
          output = "/testTerraform/integratesResources";
          gitlabExtra = gitlabTestInfra;
        }
        {
          output = "/testTerraform/integratesSecrets";
          gitlabExtra = gitlabTestInfra;
        }
      ];
    };
  };
}
