# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0
{gitlabCi, ...}: let
  gitlabBranchNotTrunk = gitlabCi.rules.branchNot "trunk";

  gitlabTitleMatchingReviews = gitlabCi.rules.titleMatching "^(all|reviews)";

  gitlabOnlyDev = [
    gitlabBranchNotTrunk
    gitlabCi.rules.notMrs
    gitlabCi.rules.notSchedules
    gitlabCi.rules.notTriggers
    gitlabTitleMatchingReviews
  ];

  gitlabLint = {
    rules = gitlabOnlyDev;
    stage = "lint-code";
    tags = ["small"];
  };
in {
  pipelines = {
    reviews = {
      gitlabPath = "/reviews/gitlab-ci.yaml";
      jobs = [
        {
          output = "/lintPython/dirOfModules/reviews";
          gitlabExtra = gitlabLint;
        }
      ];
    };
  };
}
