{ gitlabCi
, ...
}:
let
  gitlabBranchNotMaster = gitlabCi.rules.branchNot "master";

  gitlabTitleMatchingReviews = gitlabCi.rules.titleMatching "^(all|reviews)";

  gitlabOnlyDev = [
    gitlabBranchNotMaster
    gitlabCi.rules.notMrs
    gitlabCi.rules.notSchedules
    gitlabCi.rules.notTriggers
    gitlabTitleMatchingReviews
  ];

  gitlabLint = {
    rules = gitlabOnlyDev;
    stage = "lint-code";
    tags = [ "autoscaling" ];
  };
in
{
  pipelines = {
    reviews = {
      gitlabPath = "/makes/reviews/gitlab-ci.yaml";
      jobs = [
        {
          output = "/lintPython/dirOfModules/reviews";
          gitlabExtra = gitlabLint;
        }
      ];
    };
  };
}
