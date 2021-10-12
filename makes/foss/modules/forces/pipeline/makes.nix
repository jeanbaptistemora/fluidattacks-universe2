{ gitlabCi
, ...
}:
let
  gitlabBranchNotMaster = gitlabCi.rules.branchNot "master";
  gitlabBranchMaster = gitlabCi.rules.branch "master";

  gitlabTitleMatchingMakes = gitlabCi.rules.titleMatching "^(all|forces)";

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

  gitlabDeployApp = {
    rules = gitlabOnlyMaster;
    stage = "deploy-app";
    tags = [ "autoscaling" ];
  };
  gitlabDeployAppDev = {
    rules = gitlabOnlyDev;
    stage = "build";
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
  gitlabTest = {
    rules = gitlabOnlyDev;
    stage = "test-code";
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
    forces = {
      gitlabPath = "/makes/foss/modules/forces/gitlab-ci.yaml";
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
          output = "/deployTerraform/forces";
          gitlabExtra = gitlabDeployInfra;
        }
        {
          output = "/forces/process-groups";
          gitlabExtra = {
            only.refs = [ "schedules" ];
            only.variables = [ "$forces_process_groups" ];
            stage = "scheduler";
            tags = [ "autoscaling" ];
          };
        }
        {
          output = "/forces/process-groups-break";
          gitlabExtra = {
            only.refs = [ "schedules" ];
            only.variables = [ "$forces_process_groups_break" ];
            stage = "scheduler";
            tags = [ "autoscaling" ];
          };
        }
        {
          output = "/forces/test";
          gitlabExtra = gitlabTest;
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
          output = "/lintTerraform/forces";
          gitlabExtra = gitlabLint;
        }
        {
          output = "/pipelineOnGitlab/forces";
          gitlabExtra = gitlabLint;
        }
        {
          output = "/testTerraform/forces";
          gitlabExtra = gitlabTestInfra;
        }
      ];
    };
  };
}
