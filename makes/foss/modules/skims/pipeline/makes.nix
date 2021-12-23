{ gitlabCi
, inputs
, ...
}:
let
  gitlabBranchNotMaster = gitlabCi.rules.branchNot "master";
  gitlabBranchMaster = gitlabCi.rules.branch "master";

  gitlabTitleMatchingSkims = gitlabCi.rules.titleMatching "^(all|skims)";

  gitlabOnlyMaster = [
    gitlabBranchMaster
    gitlabCi.rules.notSchedules
    gitlabCi.rules.notTriggers
    gitlabTitleMatchingSkims
  ];
  gitlabOnlyDev = [
    gitlabBranchNotMaster
    gitlabCi.rules.notMrs
    gitlabCi.rules.notSchedules
    gitlabCi.rules.notTriggers
    gitlabTitleMatchingSkims
  ];

  gitlabDeployApp = {
    rules = gitlabOnlyMaster;
    stage = "deploy-app";
    tags = [ "autoscaling" ];
  };
  gitlabDeployInfra = {
    resource_group = "$CI_JOB_NAME";
    rules = gitlabOnlyMaster;
    stage = "deploy-infra";
    tags = [ "autoscaling" ];
  };
  gitlabLint = {
    rules = gitlabOnlyDev;
    stage = "lint-code";
    tags = [ "autoscaling" ];
  };
  gitlabTest = {
    rules = gitlabOnlyDev;
    stage = "test-code";
    tags = [ "autoscaling" ];
  };
  gitlabTestFuntional = {
    rules = gitlabOnlyDev;
    stage = "post-deploy";
    tags = [ "autoscaling" ];
    resource_group = "$CI_COMMIT_REF_NAME-$CI_JOB_NAME";
    needs = [ "/integrates/back/deploy/dev" ];
  };
  gitlabTestInfra = {
    rules = gitlabOnlyDev;
    stage = "test-infra";
    tags = [ "autoscaling" ];
  };
  categoriesIntegrates = [
    "functional"
    "cli"
  ];
in
{
  pipelines = {
    skims = {
      gitlabPath = "/makes/foss/modules/skims/gitlab-ci.yaml";
      jobs = [
        {
          output = "/computeOnAwsBatch/skimsOwaspBenchmarkAndUpload";
          gitlabExtra = {
            rules = [
              (gitlabCi.rules.schedules)
              (gitlabCi.rules.varIsDefined "skims_benchmark_on_aws")
              (gitlabCi.rules.always)
            ];
            stage = "scheduler";
            tags = [ "autoscaling" ];
          };
        }
        {
          output = "/deployContainerImage/skimsProd";
          gitlabExtra = gitlabDeployApp;
        }
        {
          output = "/skims/translations-fields";
          gitlabExtra = gitlabTest;
        }
        {
          output = "/deployContainerImage/skimsProcessGroup";
          gitlabExtra = gitlabDeployApp;
        }
        {
          output = "/deployTerraform/skims";
          gitlabExtra = gitlabDeployInfra;
        }
        {
          output = "/lintPython/dirOfModules/skims";
          gitlabExtra = gitlabLint;
        }
        {
          output = "/lintPython/imports/skims";
          gitlabExtra = gitlabLint;
        }
        {
          output = "/lintPython/module/skimsTest";
          gitlabExtra = gitlabLint;
        }
        {
          output = "/lintPython/module/skimsTestMocksHttp";
          gitlabExtra = gitlabLint;
        }
        {
          output = "/lintPython/module/skimsProcessGroup";
          gitlabExtra = gitlabLint;
        }
        {
          output = "/lintTerraform/skims";
          gitlabExtra = gitlabLint;
        }
      ]
      ++ (builtins.map
        (category:
          {
            output = "/testPython/skims@${category}";
            gitDepth =
              if category == "unittesting"
              then 0
              else 1;
            gitlabExtra = (if builtins.elem category categoriesIntegrates
            then gitlabTestFuntional
            else gitlabTest);
          })
        (builtins.filter
          (category: category != "_" && category != "all")
          (inputs.skimsTestPythonCategories)))
      ++ [
        {
          output = "/skims/test/cli";
          gitlabExtra = gitlabTestFuntional;
        }
        {
          output = "/testTerraform/skims";
          gitlabExtra = gitlabTestInfra;
        }
        {
          output = "/securePythonWithBandit/skims";
          gitlabExtra = gitlabLint;
        }
      ];
    };
  };
}
