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
              (gitlabCi.rules.varIsDefined "integrates_scheduler_machine_queue_all")
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
          output = "/deployTerraform/makesStatus";
          gitlabExtra = gitlabDeployInfra;
        }
        {
          output = "/deployTerraform/makesUsersDev";
          gitlabExtra = gitlabDeployInfra;
        }
        {
          output = "/deployTerraform/makesUsersProdAirs";
          gitlabExtra = gitlabDeployInfra;
        }
        {
          output = "/deployTerraform/makesUsersProdDocs";
          gitlabExtra = gitlabDeployInfra;
        }
        {
          output = "/deployTerraform/makesUsersProdForces";
          gitlabExtra = gitlabDeployInfra;
        }
        {
          output = "/deployTerraform/makesUsersProdIntegrates";
          gitlabExtra = gitlabDeployInfra;
        }
        {
          output = "/deployTerraform/makesUsersProdMakes";
          gitlabExtra = gitlabDeployInfra;
        }
        {
          output = "/deployTerraform/makesUsersProdMelts";
          gitlabExtra = gitlabDeployInfra;
        }
        {
          output = "/deployTerraform/makesUsersProdObserves";
          gitlabExtra = gitlabDeployInfra;
        }
        {
          output = "/deployTerraform/makesUsersProdServices";
          gitlabExtra = gitlabDeployInfra;
        }
        {
          output = "/deployTerraform/makesUsersProdSkims";
          gitlabExtra = gitlabDeployInfra;
        }
        {
          output = "/deployTerraform/makesUsersProdSorts";
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
          output = "/lintTerraform/makesStatus";
          gitlabExtra = gitlabLint;
        }
        {
          output = "/lintTerraform/makesUsersDev";
          gitlabExtra = gitlabLint;
        }
        {
          output = "/lintTerraform/makesUsersProdAirs";
          gitlabExtra = gitlabLint;
        }
        {
          output = "/lintTerraform/makesUsersProdDocs";
          gitlabExtra = gitlabLint;
        }
        {
          output = "/lintTerraform/makesUsersProdForces";
          gitlabExtra = gitlabLint;
        }
        {
          output = "/lintTerraform/makesUsersProdIntegrates";
          gitlabExtra = gitlabLint;
        }
        {
          output = "/lintTerraform/makesUsersProdMakes";
          gitlabExtra = gitlabLint;
        }
        {
          output = "/lintTerraform/makesUsersProdMelts";
          gitlabExtra = gitlabLint;
        }
        {
          output = "/lintTerraform/makesUsersProdObserves";
          gitlabExtra = gitlabLint;
        }
        {
          output = "/lintTerraform/makesUsersProdServices";
          gitlabExtra = gitlabLint;
        }
        {
          output = "/lintTerraform/makesUsersProdSkims";
          gitlabExtra = gitlabLint;
        }
        {
          output = "/lintTerraform/makesUsersProdSorts";
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
          output = "/makes/criteria/skims-sync";
          gitlabExtra = gitlabTestCode;
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
          output = "/taintTerraform/makesUsersDevKey1";
          gitlabExtra = gitlabRotateUsersKeys1;
        }
        {
          output = "/taintTerraform/makesUsersDevKey2";
          gitlabExtra = gitlabRotateUsersKeys2;
        }
        {
          output = "/taintTerraform/makesUsersProdAirsKeys1";
          gitlabExtra = gitlabRotateUsersKeys1;
        }
        {
          output = "/taintTerraform/makesUsersProdAirsKeys2";
          gitlabExtra = gitlabRotateUsersKeys2;
        }
        {
          output = "/taintTerraform/makesUsersProdDocsKeys1";
          gitlabExtra = gitlabRotateUsersKeys1;
        }
        {
          output = "/taintTerraform/makesUsersProdDocsKeys2";
          gitlabExtra = gitlabRotateUsersKeys2;
        }
        {
          output = "/taintTerraform/makesUsersProdForcesKeys1";
          gitlabExtra = gitlabRotateUsersKeys1;
        }
        {
          output = "/taintTerraform/makesUsersProdForcesKeys2";
          gitlabExtra = gitlabRotateUsersKeys2;
        }
        {
          output = "/taintTerraform/makesUsersProdIntegratesKeys1";
          gitlabExtra = gitlabRotateUsersKeys1;
        }
        {
          output = "/taintTerraform/makesUsersProdIntegratesKeys2";
          gitlabExtra = gitlabRotateUsersKeys2;
        }
        {
          output = "/taintTerraform/makesUsersProdMakesKeys1";
          gitlabExtra = gitlabRotateUsersKeys1;
        }
        {
          output = "/taintTerraform/makesUsersProdMakesKeys2";
          gitlabExtra = gitlabRotateUsersKeys2;
        }
        {
          output = "/taintTerraform/makesUsersProdMeltsKeys1";
          gitlabExtra = gitlabRotateUsersKeys1;
        }
        {
          output = "/taintTerraform/makesUsersProdMeltsKeys2";
          gitlabExtra = gitlabRotateUsersKeys2;
        }
        {
          output = "/taintTerraform/makesUsersProdObservesKeys1";
          gitlabExtra = gitlabRotateUsersKeys1;
        }
        {
          output = "/taintTerraform/makesUsersProdObservesKeys2";
          gitlabExtra = gitlabRotateUsersKeys2;
        }
        {
          output = "/taintTerraform/makesUsersProdServicesKeys1";
          gitlabExtra = gitlabRotateUsersKeys1;
        }
        {
          output = "/taintTerraform/makesUsersProdServicesKeys2";
          gitlabExtra = gitlabRotateUsersKeys2;
        }
        {
          output = "/taintTerraform/makesUsersProdSkimsKeys1";
          gitlabExtra = gitlabRotateUsersKeys1;
        }
        {
          output = "/taintTerraform/makesUsersProdSkimsKeys2";
          gitlabExtra = gitlabRotateUsersKeys2;
        }
        {
          output = "/taintTerraform/makesUsersProdSortsKeys1";
          gitlabExtra = gitlabRotateUsersKeys1;
        }
        {
          output = "/taintTerraform/makesUsersProdSortsKeys2";
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
          output = "/testTerraform/makesStatus";
          gitlabExtra = gitlabTestInfra;
        }
        {
          output = "/testTerraform/makesUsersDev";
          gitlabExtra = gitlabTestInfra;
        }
        {
          output = "/testTerraform/makesUsersProdAirs";
          gitlabExtra = gitlabTestInfra;
        }
        {
          output = "/testTerraform/makesUsersProdDocs";
          gitlabExtra = gitlabTestInfra;
        }
        {
          output = "/testTerraform/makesUsersProdForces";
          gitlabExtra = gitlabTestInfra;
        }
        {
          output = "/testTerraform/makesUsersProdIntegrates";
          gitlabExtra = gitlabTestInfra;
        }
        {
          output = "/testTerraform/makesUsersProdMakes";
          gitlabExtra = gitlabTestInfra;
        }
        {
          output = "/testTerraform/makesUsersProdMelts";
          gitlabExtra = gitlabTestInfra;
        }
        {
          output = "/testTerraform/makesUsersProdObserves";
          gitlabExtra = gitlabTestInfra;
        }
        {
          output = "/testTerraform/makesUsersProdServices";
          gitlabExtra = gitlabTestInfra;
        }
        {
          output = "/testTerraform/makesUsersProdSkims";
          gitlabExtra = gitlabTestInfra;
        }
        {
          output = "/testTerraform/makesUsersProdSorts";
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
