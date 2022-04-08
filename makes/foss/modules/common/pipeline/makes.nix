{gitlabCi, ...}: let
  gitlabBranchNotMaster = gitlabCi.rules.branchNot "master";
  gitlabBranchMaster = gitlabCi.rules.branch "master";

  gitlabTitleMatchingCommon = gitlabCi.rules.titleMatching "^(all|common)";

  gitlabOnlyMaster = [
    gitlabBranchMaster
    gitlabCi.rules.notSchedules
    gitlabCi.rules.notTriggers
    gitlabTitleMatchingCommon
  ];
  gitlabOnlyDev = [
    gitlabBranchNotMaster
    gitlabCi.rules.notMrs
    gitlabCi.rules.notSchedules
    gitlabCi.rules.notTriggers
    gitlabTitleMatchingCommon
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
  gitlabRotateUsersKeys1 = {
    rules = [
      gitlabCi.rules.schedules
      (gitlabCi.rules.varIsDefined "common_users_rotate_even")
      gitlabCi.rules.always
    ];
    stage = "rotation";
    tags = ["autoscaling"];
  };
  gitlabRotateUsersKeys2 = {
    rules = [
      gitlabCi.rules.schedules
      (gitlabCi.rules.varIsDefined "common_users_rotate_odd")
      gitlabCi.rules.always
    ];
    stage = "rotation";
    tags = ["autoscaling"];
  };
  gitlabTestCode = {
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
    common = {
      gitlabPath = "/makes/foss/modules/common/gitlab-ci.yaml";
      jobs = [
        {
          output = "/docs/generate/criteria";
          gitlabExtra = {
            rules = gitlabOnlyDev;
            stage = "build";
            tags = ["autoscaling"];
          };
        }
        {
          output = "/deployTerraform/commonCompute";
          gitlabExtra = gitlabDeployInfra;
        }
        {
          output = "/deployTerraform/commonDns";
          gitlabExtra = gitlabDeployInfra;
        }
        {
          output = "/deployTerraform/commonFoss";
          gitlabExtra = gitlabDeployInfra;
        }
        {
          output = "/deployTerraform/commonKubernetes";
          gitlabExtra = gitlabDeployInfra;
        }
        {
          output = "/deployTerraform/commonOkta";
          gitlabExtra = gitlabDeployInfra;
        }
        {
          output = "/deployTerraform/commonStatus";
          gitlabExtra = gitlabDeployInfra;
        }
        {
          output = "/deployTerraform/commonVpc";
          gitlabExtra = gitlabDeployInfra;
        }
        {
          output = "/deployTerraform/commonVpn";
          gitlabExtra = gitlabDeployInfra;
        }
        {
          output = "/lintTerraform/commonCi";
          gitlabExtra = gitlabLint;
        }
        {
          output = "/lintTerraform/commonCompute";
          gitlabExtra = gitlabLint;
        }
        {
          output = "/lintTerraform/commonDns";
          gitlabExtra = gitlabLint;
        }
        {
          output = "/lintTerraform/commonFoss";
          gitlabExtra = gitlabLint;
        }
        {
          output = "/lintTerraform/commonKubernetes";
          gitlabExtra = gitlabLint;
        }
        {
          output = "/lintTerraform/commonOkta";
          gitlabExtra = gitlabLint;
        }
        {
          output = "/lintTerraform/commonStatus";
          gitlabExtra = gitlabLint;
        }
        {
          output = "/lintTerraform/commonUsers";
          gitlabExtra = gitlabLint;
        }
        {
          output = "/lintTerraform/commonVpc";
          gitlabExtra = gitlabLint;
        }
        {
          output = "/lintTerraform/commonVpn";
          gitlabExtra = gitlabLint;
        }
        {
          output = "/lintWithAjv/common/criteria/compliance";
          gitlabExtra = gitlabLint;
        }
        {
          output = "/lintWithAjv/common/criteria/requirements";
          gitlabExtra = gitlabLint;
        }
        {
          output = "/lintWithAjv/common/criteria/vulnerabilities";
          gitlabExtra = gitlabLint;
        }
        {
          output = "/common/criteria/skims-sync";
          gitlabExtra = gitlabTestCode;
        }
        {
          output = "/common/criteria/test";
          gitlabExtra = gitlabTestCode;
        }
        {
          output = "/common/criteria/unreferenced";
          gitlabExtra = gitlabTestCode;
        }
        {
          output = "/pipelineOnGitlab/common";
          gitlabExtra = gitlabLint;
        }
        {
          output = "/taintTerraform/commonUsersKeys1";
          gitlabExtra = gitlabRotateUsersKeys1;
        }
        {
          output = "/taintTerraform/commonUsersKeys2";
          gitlabExtra = gitlabRotateUsersKeys2;
        }
        {
          output = "/testTerraform/commonCi";
          gitlabExtra = gitlabTestInfra;
        }
        {
          output = "/testTerraform/commonCompute";
          gitlabExtra = gitlabTestInfra;
        }
        {
          output = "/testTerraform/commonCompute";
          gitlabExtra = gitlabTestInfra;
        }
        {
          output = "/testTerraform/commonDns";
          gitlabExtra = gitlabTestInfra;
        }
        {
          output = "/testTerraform/commonFoss";
          gitlabExtra = gitlabTestInfra;
        }
        {
          output = "/testTerraform/commonKubernetes";
          gitlabExtra = gitlabTestInfra;
        }
        {
          output = "/testTerraform/commonOkta";
          gitlabExtra = gitlabTestInfra;
        }
        {
          output = "/testTerraform/commonStatus";
          gitlabExtra = gitlabTestInfra;
        }
        {
          output = "/testTerraform/commonUsers";
          gitlabExtra = gitlabTestInfra;
        }
        {
          output = "/testTerraform/commonVpc";
          gitlabExtra = gitlabTestInfra;
        }
        {
          output = "/testTerraform/commonVpn";
          gitlabExtra = gitlabTestInfra;
        }
      ];
    };
  };
}
