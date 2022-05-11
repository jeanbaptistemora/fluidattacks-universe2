{
  gitlabCi,
  inputs,
  ...
}: let
  gitlabBranchMaster = gitlabCi.rules.branch "master";
  gitlabBranchNotMaster = gitlabCi.rules.branchNot "master";

  gitlabTitleMatchingObserves = gitlabCi.rules.titleMatching "^(all|observes)";

  gitlabOnlyDev = [
    gitlabBranchNotMaster
    gitlabCi.rules.notMrs
    gitlabCi.rules.notSchedules
    gitlabCi.rules.notTriggers
    gitlabTitleMatchingObserves
  ];
  gitlabOnlyMaster = [
    gitlabBranchMaster
    gitlabCi.rules.notSchedules
    gitlabCi.rules.notTriggers
    gitlabTitleMatchingObserves
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
  gitlabTestInfra = {
    rules = gitlabOnlyDev;
    stage = "test-infra";
    tags = ["autoscaling"];
  };
  gitlabTestCode = {
    rules = gitlabOnlyDev;
    stage = "test-code";
    tags = ["autoscaling"];
  };
  # new standard
  index = inputs.observesIndex;
  pkgTargets = with index; [
    service.batch_stability
    tap.checkly
  ];
  genPkgJobs = pkg: [
    {
      output = pkg.check.arch;
      gitlabExtra = gitlabLint;
    }
    {
      output = pkg.check.types;
      gitlabExtra = gitlabLint;
    }
    {
      output = pkg.check.tests;
      gitlabExtra = gitlabTestCode;
    }
  ];
  pkgsJobs = builtins.concatLists (map genPkgJobs pkgTargets);
  # legacy standard
  targets = with index; [
    etl.code
    service.scheduler
  ];
  lintJobsOutputs = map (x: x.lint) targets;
  lintJobs =
    map (
      output: {
        inherit output;
        gitlabExtra = gitlabLint;
      }
    )
    lintJobsOutputs;
  testJobsOutputs = map (x: x.test) targets;
  testJobs =
    map (
      output: {
        inherit output;
        gitlabExtra = gitlabTestCode;
      }
    )
    testJobsOutputs;
in {
  pipelines = {
    observes = {
      gitlabPath = "/observes/gitlab-ci.yaml";
      jobs =
        lintJobs
        ++ testJobs
        ++ pkgsJobs
        ++ [
          {
            output = "/deployTerraform/observes";
            gitlabExtra = gitlabDeployInfra;
          }
          {
            output = "/lintPython/imports/observesArch";
            gitlabExtra = gitlabLint;
          }
          {
            output = "/lintPython/imports/observesCommonPaginator";
            gitlabExtra = gitlabLint;
          }
          {
            output = "/lintPython/imports/observesCommonSingerIo";
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
            output = "/lintPython/imports/observesTapAnnounceKit";
            gitlabExtra = gitlabLint;
          }
          {
            output = "/lintPython/imports/observesTapBugsnag";
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
            output = "/lintPython/module/observesCommonPaginator";
            gitlabExtra = gitlabLint;
          }
          {
            output = "/lintPython/module/observesCommonSingerIo";
            gitlabExtra = gitlabLint;
          }
          {
            output = "/lintPython/module/observesCommonSingerIoTests";
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
            output = "/lintPython/module/observesTapAnnounceKit";
            gitlabExtra = gitlabLint;
          }
          {
            output = "/lintPython/module/observesTapAnnounceKitTests";
            gitlabExtra = gitlabLint;
          }
          {
            output = "/lintPython/module/observesTapBugsnag";
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
            output = "/lintPython/module/observesTapDynamo";
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
          {
            output = "/lintTerraform/observes";
            gitlabExtra = gitlabLint;
          }
          {
            output = "/pipelineOnGitlab/observes";
            gitlabExtra = gitlabLint;
          }
          {
            output = "/observes/singer/tap-announcekit/fx-test";
            gitlabExtra = gitlabTestCode;
          }
          {
            output = "/observes/common/singer-io/test";
            gitlabExtra = gitlabTestCode;
          }
          {
            output = "/observes/singer/tap-announcekit/test";
            gitlabExtra = gitlabTestCode;
          }
          {
            output = "/observes/singer/tap-csv/test";
            gitlabExtra = gitlabTestCode;
          }
          {
            output = "/observes/singer/tap-gitlab/test";
            gitlabExtra = gitlabTestCode;
          }
          {
            output = "/observes/singer/tap-mailchimp/test";
            gitlabExtra = gitlabTestCode;
          }
          {
            output = "/observes/singer/tap-mixpanel/test";
            gitlabExtra = gitlabTestCode;
          }
          {
            output = "/testTerraform/observes";
            gitlabExtra = gitlabTestInfra;
          }
        ];
    };
  };
}
