# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0
{gitlabCi, ...}: let
  gitlabBranchNotTrunk = gitlabCi.rules.branchNot "trunk";
  gitlabBranchTrunk = gitlabCi.rules.branch "trunk";

  gitlabTitleMatchingMakes = gitlabCi.rules.titleMatching "^(all|forces)";

  gitlabOnlyProd = [
    gitlabBranchTrunk
    gitlabCi.rules.notSchedules
    gitlabCi.rules.notTriggers
    gitlabTitleMatchingMakes
  ];
  gitlabOnlyDev = [
    gitlabBranchNotTrunk
    gitlabCi.rules.notMrs
    gitlabCi.rules.notSchedules
    gitlabCi.rules.notTriggers
    gitlabTitleMatchingMakes
  ];

  gitlabDeployApp = {
    rules = gitlabOnlyProd;
    stage = "deploy-app";
    tags = ["small"];
  };
  gitlabDeployAppDev = {
    rules = gitlabOnlyDev;
    stage = "build";
    tags = ["small"];
  };
  gitlabLint = {
    rules = gitlabOnlyDev;
    stage = "lint-code";
    tags = ["small"];
  };
  gitlabTest = {
    rules = gitlabOnlyDev;
    stage = "post-deploy";
    tags = ["small"];
    variables = {
      API_ENDPOINT = "https://$CI_COMMIT_REF_NAME.app.fluidattacks.com/api";
    };
  };
in {
  pipelines = {
    forces = {
      gitlabPath = "/forces/gitlab-ci.yaml";
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
          output = "/forces/test";
          gitlabExtra =
            gitlabTest
            // {
              needs = ["/integrates/back/deploy/dev"];
            };
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
          output = "/pipelineOnGitlab/forces";
          gitlabExtra = gitlabLint;
        }
      ];
    };
  };
}
