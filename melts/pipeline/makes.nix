# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0
{gitlabCi, ...}: let
  gitlabBranchNotTrunk = gitlabCi.rules.branchNot "trunk";

  gitlabTitleMatchingMelts = gitlabCi.rules.titleMatching "^(all|melts)";

  gitlabOnlyDev = [
    gitlabBranchNotTrunk
    gitlabCi.rules.notMrs
    gitlabCi.rules.notSchedules
    gitlabCi.rules.notTriggers
    gitlabTitleMatchingMelts
  ];

  gitlabLint = {
    rules = gitlabOnlyDev;
    stage = "lint-code";
    tags = ["small"];
  };
in {
  pipelines = {
    melts = {
      gitlabPath = "/melts/gitlab-ci.yaml";
      jobs = [
        {
          output = "/lintPython/module/melts";
          gitlabExtra = gitlabLint;
        }
        {
          output = "/lintPython/module/meltsTest";
          gitlabExtra = gitlabLint;
        }
        {
          output = "/melts/test";
          gitlabExtra = {
            rules = gitlabOnlyDev;
            services = [
              {
                alias = "localstack";
                name = "localstack/localstack";
              }
            ];
            stage = "test-code";
            tags = ["large"];
            variables = {
              SERVICES = "s3";
              HOSTNAME_EXTERNAL = "localstack";
            };
          };
        }
      ];
    };
  };
}
