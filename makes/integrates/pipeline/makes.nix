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
      gitlabPath = "/makes/integrates/gitlab-ci.yaml";
      jobs = [
        {
          output = "/deployTerraform/integratesBackups";
          gitlabExtra = gitlabDeployInfra;
        }
        {
          output = "/lintPython/dirOfModules/integrates";
          gitlabExtra = gitlabLint;
        }
        {
          output = "/lintPython/dirOfModules/integratesBackChartsGenerators";
          gitlabExtra = gitlabLint;
        }
        # TODO: https://gitlab.com/fluidattacks/product/-/issues/5247
        # {
        #   output = "/lintPython/imports/integrates";
        #   gitlabExtra = gitlabLint;
        # }
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
          output = "/pipelineOnGitlab/integrates";
          gitlabExtra = gitlabLint;
        }
        {
          output = "/testTerraform/integratesBackups";
          gitlabExtra = gitlabTestInfra;
        }
      ];
    };
  };
}
