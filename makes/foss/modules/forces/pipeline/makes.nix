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
          output = "/deployTerraform/forces";
          gitlabExtra = gitlabDeployInfra;
        }
        {
          output = "/forces/process-groups";
          gitlabExtra = {
            only.refs = [ "schedules" ];
            only.variables = [ "$forces_process_groups" ];
            stage = "scheduler";
          };
        }
        {
          output = "/forces/process-groups-break";
          gitlabExtra = {
            only.refs = [ "schedules" ];
            only.variables = [ "$forces_process_groups_break" ];
            stage = "scheduler";
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
