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
    tags = ["reviews-small"];
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
