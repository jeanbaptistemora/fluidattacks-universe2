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
  gitlabRotateUsersKeys1 = {
    rules = [
      gitlabCi.rules.schedules
      (gitlabCi.rules.varIsDefined "makes_users_rotate_even")
      gitlabCi.rules.always
    ];
    stage = "rotation";
    tags = [ "autoscaling" ];
  };
  gitlabRotateUsersKeys2 = {
    rules = [
      gitlabCi.rules.schedules
      (gitlabCi.rules.varIsDefined "makes_users_rotate_odd")
      gitlabCi.rules.always
    ];
    stage = "rotation";
    tags = [ "autoscaling" ];
  };
  gitlabTestCode = {
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
    makes = {
      gitlabPath = "/makes/foss/modules/makes/gitlab-ci.yaml";
      jobs = [
        {
          output = "/docs/generate/criteria";
          gitlabExtra = {
            rules = gitlabOnlyDev;
            stage = "build";
            tags = [ "autoscaling" ];
          };
        }
        {
          output = "/deployTerraform/makesCompute";
          gitlabExtra = gitlabDeployInfra // {
            rules = [
              gitlabCi.rules.schedules
              (gitlabCi.rules.varIsDefined "integrates_scheduler_skims_queue_all")
              gitlabCi.rules.always
            ];
          };
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
          output = "/deployTerraform/makesKubernetes";
          gitlabExtra = gitlabDeployInfra;
        }
        {
          output = "/deployTerraform/makesOkta";
          gitlabExtra = gitlabDeployInfra;
        }
        {
          output = "/deployTerraform/makesSecrets";
          gitlabExtra = gitlabDeployInfra;
        }
        {
          output = "/deployTerraform/makesUsersAirs";
          gitlabExtra = gitlabDeployInfra;
        }
        {
          output = "/deployTerraform/makesUsersDocs";
          gitlabExtra = gitlabDeployInfra;
        }
        {
          output = "/deployTerraform/makesUsersForces";
          gitlabExtra = gitlabDeployInfra;
        }
        {
          output = "/deployTerraform/makesUsersIntegrates";
          gitlabExtra = gitlabDeployInfra;
        }
        {
          output = "/deployTerraform/makesUsersMelts";
          gitlabExtra = gitlabDeployInfra;
        }
        {
          output = "/deployTerraform/makesUsersMakes";
          gitlabExtra = gitlabDeployInfra;
        }
        {
          output = "/deployTerraform/makesUsersObserves";
          gitlabExtra = gitlabDeployInfra;
        }
        {
          output = "/deployTerraform/makesUsersServices";
          gitlabExtra = gitlabDeployInfra;
        }
        {
          output = "/deployTerraform/makesUsersSkims";
          gitlabExtra = gitlabDeployInfra;
        }
        {
          output = "/deployTerraform/makesUsersSorts";
          gitlabExtra = gitlabDeployInfra;
        }
        {
          output = "/deployTerraform/makesVpc";
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
          output = "/lintTerraform/makesKubernetes";
          gitlabExtra = gitlabLint;
        }
        {
          output = "/lintTerraform/makesOkta";
          gitlabExtra = gitlabLint;
        }
        {
          output = "/lintTerraform/makesSecrets";
          gitlabExtra = gitlabLint;
        }
        {
          output = "/lintTerraform/makesUsersAirs";
          gitlabExtra = gitlabLint;
        }
        {
          output = "/lintTerraform/makesUsersDocs";
          gitlabExtra = gitlabLint;
        }
        {
          output = "/lintTerraform/makesUsersForces";
          gitlabExtra = gitlabLint;
        }
        {
          output = "/lintTerraform/makesUsersIntegrates";
          gitlabExtra = gitlabLint;
        }
        {
          output = "/lintTerraform/makesUsersMakes";
          gitlabExtra = gitlabLint;
        }
        {
          output = "/lintTerraform/makesUsersMelts";
          gitlabExtra = gitlabLint;
        }
        {
          output = "/lintTerraform/makesUsersObserves";
          gitlabExtra = gitlabLint;
        }
        {
          output = "/lintTerraform/makesUsersServices";
          gitlabExtra = gitlabLint;
        }
        {
          output = "/lintTerraform/makesUsersSkims";
          gitlabExtra = gitlabLint;
        }
        {
          output = "/lintTerraform/makesUsersSorts";
          gitlabExtra = gitlabLint;
        }
        {
          output = "/lintTerraform/makesVpc";
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
          output = "/makes/criteria/test";
          gitlabExtra = gitlabTestCode;
        }
        {
          output = "/makes/criteria/unreferenced";
          gitlabExtra = gitlabTestCode;
        }
        {
          output = "/pipelineOnGitlab/makes";
          gitlabExtra = gitlabLint;
        }
        {
          output = "/taintTerraform/makesUsersAirsKeys1";
          gitlabExtra = gitlabRotateUsersKeys1;
        }
        {
          output = "/taintTerraform/makesUsersAirsKeys2";
          gitlabExtra = gitlabRotateUsersKeys2;
        }
        {
          output = "/taintTerraform/makesUsersDocsKeys1";
          gitlabExtra = gitlabRotateUsersKeys1;
        }
        {
          output = "/taintTerraform/makesUsersDocsKeys2";
          gitlabExtra = gitlabRotateUsersKeys2;
        }
        {
          output = "/taintTerraform/makesUsersForcesKeys1";
          gitlabExtra = gitlabRotateUsersKeys1;
        }
        {
          output = "/taintTerraform/makesUsersForcesKeys2";
          gitlabExtra = gitlabRotateUsersKeys2;
        }
        {
          output = "/taintTerraform/makesUsersIntegratesKeys1";
          gitlabExtra = gitlabRotateUsersKeys1;
        }
        {
          output = "/taintTerraform/makesUsersIntegratesKeys2";
          gitlabExtra = gitlabRotateUsersKeys2;
        }
        {
          output = "/taintTerraform/makesUsersMakesKeys1";
          gitlabExtra = gitlabRotateUsersKeys1;
        }
        {
          output = "/taintTerraform/makesUsersMakesKeys2";
          gitlabExtra = gitlabRotateUsersKeys2;
        }
        {
          output = "/taintTerraform/makesUsersMeltsKeys1";
          gitlabExtra = gitlabRotateUsersKeys1;
        }
        {
          output = "/taintTerraform/makesUsersMeltsKeys2";
          gitlabExtra = gitlabRotateUsersKeys2;
        }
        {
          output = "/taintTerraform/makesUsersObservesKeys1";
          gitlabExtra = gitlabRotateUsersKeys1;
        }
        {
          output = "/taintTerraform/makesUsersObservesKeys2";
          gitlabExtra = gitlabRotateUsersKeys2;
        }
        {
          output = "/taintTerraform/makesUsersServicesKeys1";
          gitlabExtra = gitlabRotateUsersKeys1;
        }
        {
          output = "/taintTerraform/makesUsersServicesKeys2";
          gitlabExtra = gitlabRotateUsersKeys2;
        }
        {
          output = "/taintTerraform/makesUsersSkimsKeys1";
          gitlabExtra = gitlabRotateUsersKeys1;
        }
        {
          output = "/taintTerraform/makesUsersSkimsKeys2";
          gitlabExtra = gitlabRotateUsersKeys2;
        }
        {
          output = "/taintTerraform/makesUsersSortsKeys1";
          gitlabExtra = gitlabRotateUsersKeys1;
        }
        {
          output = "/taintTerraform/makesUsersSortsKeys2";
          gitlabExtra = gitlabRotateUsersKeys2;
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
          output = "/testTerraform/makesKubernetes";
          gitlabExtra = gitlabTestInfra;
        }
        {
          output = "/testTerraform/makesOkta";
          gitlabExtra = gitlabTestInfra;
        }
        {
          output = "/testTerraform/makesSecrets";
          gitlabExtra = gitlabTestInfra;
        }
        {
          output = "/testTerraform/makesUsersAirs";
          gitlabExtra = gitlabTestInfra;
        }
        {
          output = "/testTerraform/makesUsersDocs";
          gitlabExtra = gitlabTestInfra;
        }
        {
          output = "/testTerraform/makesUsersForces";
          gitlabExtra = gitlabTestInfra;
        }
        {
          output = "/testTerraform/makesUsersIntegrates";
          gitlabExtra = gitlabTestInfra;
        }
        {
          output = "/testTerraform/makesUsersMakes";
          gitlabExtra = gitlabTestInfra;
        }
        {
          output = "/testTerraform/makesUsersMelts";
          gitlabExtra = gitlabTestInfra;
        }
        {
          output = "/testTerraform/makesUsersObserves";
          gitlabExtra = gitlabTestInfra;
        }
        {
          output = "/testTerraform/makesUsersServices";
          gitlabExtra = gitlabTestInfra;
        }
        {
          output = "/testTerraform/makesUsersSkims";
          gitlabExtra = gitlabTestInfra;
        }
        {
          output = "/testTerraform/makesUsersSorts";
          gitlabExtra = gitlabTestInfra;
        }
        {
          output = "/testTerraform/makesVpc";
          gitlabExtra = gitlabTestInfra;
        }
      ];
    };
  };
}
