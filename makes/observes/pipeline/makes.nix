{ gitlabCi
, ...
}:
let
  gitlabBranchNotMaster = gitlabCi.rules.branchNot "master";

  gitlabTitleMatchingObserves = gitlabCi.rules.titleMatching "^(all|observes)";

  gitlabOnlyDev = [
    gitlabBranchNotMaster
    gitlabCi.rules.notMrs
    gitlabCi.rules.notSchedules
    gitlabCi.rules.notTriggers
    gitlabTitleMatchingObserves
  ];

  gitlabLint = {
    rules = gitlabOnlyDev;
    stage = "lint-code";
    tags = [ "autoscaling" ];
  };
in
{
  pipelines = {
    observes = {
      gitlabPath = "/makes/observes/gitlab-ci.yaml";
      jobs = [
        {
          output = "/lintPython/imports/observesArch";
          gitlabExtra = gitlabLint;
        }
        {
          output = "/lintPython/imports/observesCommonPaginator";
          gitlabExtra = gitlabLint;
        }
        {
          output = "/lintPython/imports/observesCommonPostgresClient";
          gitlabExtra = gitlabLint;
        }
        {
          output = "/lintPython/imports/observesServiceTimedoctorTokens";
          gitlabExtra = gitlabLint;
        }
        {
          output = "/lintPython/imports/observesTapBugsnag";
          gitlabExtra = gitlabLint;
        }
        {
          output = "/lintPython/imports/observesTapCheckly";
          gitlabExtra = gitlabLint;
        }
        {
          output = "/lintPython/imports/observesTapCsv";
          gitlabExtra = gitlabLint;
        }
        {
          output = "/lintPython/imports/observesTapDelighted";
          gitlabExtra = gitlabLint;
        }
        {
          output = "/lintPython/imports/observesTapFormstack";
          gitlabExtra = gitlabLint;
        }
        {
          output = "/lintPython/imports/observesTapGitlab";
          gitlabExtra = gitlabLint;
        }
        {
          output = "/lintPython/imports/observesTapJson";
          gitlabExtra = gitlabLint;
        }
        {
          output = "/lintPython/imports/observesTapMailchimp";
          gitlabExtra = gitlabLint;
        }
        {
          output = "/lintPython/imports/observesTapMixpanel";
          gitlabExtra = gitlabLint;
        }
        {
          output = "/lintPython/imports/observesTapTimedoctor";
          gitlabExtra = gitlabLint;
        }
        {
          output = "/lintPython/module/observesCodeEtl";
          gitlabExtra = gitlabLint;
        }
        {
          output = "/lintPython/module/observesCodeEtlTests";
          gitlabExtra = gitlabLint;
        }
        {
          output = "/lintPython/module/observesCommonPaginator";
          gitlabExtra = gitlabLint;
        }
        {
          output = "/lintPython/module/observesCommonPostgresClient";
          gitlabExtra = gitlabLint;
        }
        {
          output = "/lintPython/module/observesCommonPostgresClientTests";
          gitlabExtra = gitlabLint;
        }
        {
          output = "/lintPython/module/observesJobLastSuccess";
          gitlabExtra = gitlabLint;
        }
        {
          output = "/lintPython/module/observesJobLastSuccessTests";
          gitlabExtra = gitlabLint;
        }
        {
          output = "/lintPython/module/observesServiceBatchStability";
          gitlabExtra = gitlabLint;
        }
        {
          output = "/lintPython/module/observesServiceJobsScheduler";
          gitlabExtra = gitlabLint;
        }
        {
          output = "/lintPython/module/observesServiceMigrateTables";
          gitlabExtra = gitlabLint;
        }
        {
          output = "/lintPython/module/observesServiceTimedoctorTokens";
          gitlabExtra = gitlabLint;
        }
        {
          output = "/lintPython/module/observesStreamerZohoCrm";
          gitlabExtra = gitlabLint;
        }
        {
          output = "/lintPython/module/observesStreamerZohoCrmTests";
          gitlabExtra = gitlabLint;
        }
        {
          output = "/lintPython/module/observesTapBugsnag";
          gitlabExtra = gitlabLint;
        }
        {
          output = "/lintPython/module/observesTapCheckly";
          gitlabExtra = gitlabLint;
        }
        {
          output = "/lintPython/module/observesTapCsv";
          gitlabExtra = gitlabLint;
        }
        {
          output = "/lintPython/module/observesTapCsvTests";
          gitlabExtra = gitlabLint;
        }
        {
          output = "/lintPython/module/observesTapDelighted";
          gitlabExtra = gitlabLint;
        }
        {
          output = "/lintPython/module/observesTapFormstack";
          gitlabExtra = gitlabLint;
        }
        {
          output = "/lintPython/module/observesTapGitlab";
          gitlabExtra = gitlabLint;
        }
        {
          output = "/lintPython/module/observesTapGitlabTests";
          gitlabExtra = gitlabLint;
        }
        {
          output = "/lintPython/module/observesTapJson";
          gitlabExtra = gitlabLint;
        }
        {
          output = "/lintPython/module/observesTapMailchimp";
          gitlabExtra = gitlabLint;
        }
        {
          output = "/lintPython/module/observesTapMailchimpTests";
          gitlabExtra = gitlabLint;
        }
        {
          output = "/lintPython/module/observesTapTimedoctor";
          gitlabExtra = gitlabLint;
        }
        {
          output = "/lintPython/module/observesTargetRedshift";
          gitlabExtra = gitlabLint;
        }
      ];
    };
  };
}
