{gitlabCi, ...}: let
  gitlabBranchNotTrunk = gitlabCi.rules.branchNot "trunk";
  gitlabBranchTrunk = gitlabCi.rules.branch "trunk";

  gitlabTitleMatchingCommon = gitlabCi.rules.titleMatching "^(all|common)";

  gitlabOnlyProd = [
    gitlabBranchTrunk
    gitlabCi.rules.notSchedules
    gitlabCi.rules.notTriggers
    gitlabTitleMatchingCommon
  ];
  gitlabOnlyDev = [
    gitlabBranchNotTrunk
    gitlabCi.rules.notMrs
    gitlabCi.rules.notSchedules
    gitlabCi.rules.notTriggers
    gitlabTitleMatchingCommon
  ];

  gitlabDeployInfra = {
    resource_group = "$CI_JOB_NAME";
    rules = gitlabOnlyProd;
    stage = "deploy-infra";
    tags = ["common-small"];
  };
  gitlabLint = {
    rules = gitlabOnlyDev;
    stage = "lint-code";
    tags = ["common-small"];
  };
  gitlabTestCode = {
    rules = gitlabOnlyDev;
    stage = "test-code";
    tags = ["common-small"];
  };
  gitlabTestInfra = {
    rules = gitlabOnlyDev;
    stage = "test-infra";
    tags = ["common-small"];
  };
in {
  pipelines = {
    common = {
      gitlabPath = "/common/gitlab-ci.yaml";
      jobs = [
        {
          output = "/docs/generate/criteria";
          gitlabExtra = {
            rules = gitlabOnlyDev;
            stage = "build";
            tags = ["common-small"];
          };
        }
        {
          output = "/deployTerraform/commonCi";
          gitlabExtra = gitlabDeployInfra;
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
          output = "/deployTerraform/commonK8s";
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
          output = "/deployTerraform/commonUsers";
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
          output = "/common/utils/retrieves/deploy";
          gitlabExtra = gitlabDeployInfra;
        }
        {
          output = "/secureKubernetesWithRbacPolice/commonK8s";
          gitlabExtra = gitlabDeployInfra // {allow_failure = true;};
        }
        {
          output = "/lintPython/module/commonComputeScheduleParseTerraform";
          gitlabExtra = gitlabLint;
        }
        {
          output = "/lintPython/module/commonOktaParse";
          gitlabExtra = gitlabLint;
        }
        {
          output = "/lintPython/module/commonUtilsGitSelf";
          gitlabExtra = gitlabLint;
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
          output = "/lintTerraform/commonK8s";
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
          output = "/lintWithAjv/common/compute/arch/sizes";
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
          output = "/common/criteria/test/base";
          gitlabExtra = gitlabTestCode;
        }
        {
          output = "/common/criteria/test/skims-sync";
          gitlabExtra = gitlabTestCode;
        }
        {
          output = "/common/criteria/test/unreferenced";
          gitlabExtra = gitlabTestCode;
        }
        {
          output = "/pipelineOnGitlab/common";
          gitlabExtra = gitlabLint;
        }
        {
          output = "/common/utils/retrieves/lint";
          gitlabExtra = gitlabLint;
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
          output = "/testTerraform/commonDns";
          gitlabExtra = gitlabTestInfra;
        }
        {
          output = "/testTerraform/commonFoss";
          gitlabExtra = gitlabTestInfra;
        }
        {
          output = "/testTerraform/commonK8s";
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
