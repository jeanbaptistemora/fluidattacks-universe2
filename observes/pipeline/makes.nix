{
  gitlabCi,
  inputs,
  ...
}: let
  gitlabBranchTrunk = gitlabCi.rules.branch "trunk";
  gitlabBranchNotTrunk = gitlabCi.rules.branchNot "trunk";

  gitlabTitleMatchingObserves = gitlabCi.rules.titleMatching "^(all|observes)";

  gitlabOnlyDev = [
    gitlabBranchNotTrunk
    gitlabCi.rules.notMrs
    gitlabCi.rules.notSchedules
    gitlabCi.rules.notTriggers
    gitlabTitleMatchingObserves
  ];
  gitlabOnlyProd = [
    gitlabBranchTrunk
    gitlabCi.rules.notSchedules
    gitlabCi.rules.notTriggers
    gitlabTitleMatchingObserves
  ];

  gitlabDeployInfra = {
    resource_group = "$CI_JOB_NAME";
    rules = gitlabOnlyProd;
    stage = "deploy-infra";
    tags = ["small"];
  };
  gitlabBuild = {
    rules = gitlabOnlyDev;
    stage = "build";
    tags = ["small"];
  };
  gitlabLint = {
    rules = gitlabOnlyDev;
    stage = "lint-code";
    tags = ["small"];
  };
  gitlabTestInfra = {
    rules = gitlabOnlyDev;
    stage = "test-infra";
    tags = ["small"];
  };
  gitlabTestCode = {
    rules = gitlabOnlyDev;
    stage = "test-code";
    tags = ["small"];
  };
  # new standard
  index = inputs.observesIndex;
  std_pkgs = with index; [
    common.asm_dal
    common.utils_logger_2
    etl.code
    etl.dynamo
    service.batch_stability
    service.scheduler
    service.success_indicators
    tap.checkly
    tap.dynamo
    tap.gitlab
    tap.json
    tap.mandrill
    target.s3
    target.redshift_2
  ];
  _if_exists = attrs: key: gitlabExtra:
    if builtins.hasAttr key attrs
    then [
      {
        inherit gitlabExtra;
        output = attrs."${key}";
      }
    ]
    else [];
  genPkgJobs = pkg: let
    arch_check = _if_exists pkg.check "arch" gitlabLint;
    types_check = _if_exists pkg.check "types" gitlabLint;
    tests_check = _if_exists pkg.check "tests" gitlabTestCode;
    run_check = _if_exists pkg.check "runtime" gitlabTestCode;
    env_dev = _if_exists pkg.env "dev" gitlabBuild;
  in
    arch_check ++ types_check ++ tests_check ++ run_check ++ env_dev;
  pkgsJobs = builtins.concatLists (map genPkgJobs std_pkgs);
in {
  pipelines = {
    observes = {
      gitlabPath = "/observes/gitlab-ci.yaml";
      jobs =
        pkgsJobs
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
            output = "/lintPython/imports/observesTapMailchimp";
            gitlabExtra = gitlabLint;
          }
          {
            output = "/lintPython/imports/observesTapMatomo";
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
            output = "/lintPython/module/observesTapFormstack";
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
            output = "/lintPython/module/observesTapMatomo";
            gitlabExtra = gitlabLint;
          }
          {
            output = "/lintPython/module/observesTapMixpanel";
            gitlabExtra = gitlabLint;
          }
          {
            output = "/lintPython/module/observesTapMixpanelTests";
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
