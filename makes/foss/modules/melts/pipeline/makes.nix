{ gitlabCi
, ...
}:
let
  gitlabBranchNotMaster = gitlabCi.rules.branchNot "master";

  gitlabTitleMatchingMelts = gitlabCi.rules.titleMatching "^(all|melts)";

  gitlabOnlyDev = [
    gitlabBranchNotMaster
    gitlabCi.rules.notMrs
    gitlabCi.rules.notSchedules
    gitlabCi.rules.notTriggers
    gitlabTitleMatchingMelts
  ];

  gitlabLint = {
    rules = gitlabOnlyDev;
    stage = "lint-code";
    tags = [ "autoscaling" ];
  };
in
{
  pipelines = {
    melts = {
      gitlabPath = "/makes/foss/modules/melts/gitlab-ci.yaml";
      jobs = [
        {
          output = "/lintPython/module/melts";
          gitlabExtra = gitlabLint;
        }
        {
          output = "/lintPython/module/meltsTests";
          gitlabExtra = gitlabLint;
        }
        {
          output = "/melts/test";
          gitlabExtra = {
            rules = gitlabOnlyDev;
            services = [
              { alias = "localstack"; name = "localstack/localstack"; }
            ];
            stage = "test-code";
            tags = [ "autoscaling-large" ];
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
