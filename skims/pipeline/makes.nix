{
  gitlabCi,
  inputs,
  ...
}: let
  gitlabBranchNotTrunk = gitlabCi.rules.branchNot "trunk";
  gitlabBranchTrunk = gitlabCi.rules.branch "trunk";

  gitlabTitleMatchingSkims = gitlabCi.rules.titleMatching "^(all|skims)";

  gitlabOnlyTrunk = [
    gitlabBranchTrunk
    gitlabCi.rules.notSchedules
    gitlabCi.rules.notTriggers
    gitlabTitleMatchingSkims
  ];
  gitlabOnlyDev = [
    gitlabBranchNotTrunk
    gitlabCi.rules.notMrs
    gitlabCi.rules.notSchedules
    gitlabCi.rules.notTriggers
    gitlabTitleMatchingSkims
  ];
  gitlabOnlyDevAndTrunk = [
    gitlabCi.rules.notMrs
    gitlabCi.rules.notSchedules
    gitlabCi.rules.notTriggers
    gitlabTitleMatchingSkims
  ];

  gitlabDeployInfra = {
    resource_group = "$CI_JOB_NAME";
    rules = gitlabOnlyTrunk;
    stage = "deploy-infra";
    tags = ["skims-small"];
  };
  gitlabLint = {
    rules = gitlabOnlyDev;
    stage = "lint-code";
    tags = ["skims-small"];
  };
  gitlabTest = {
    rules = gitlabOnlyDevAndTrunk;
    stage = "test-code";
    tags = ["skims-small"];
  };
  gitlabTestInfra = {
    rules = gitlabOnlyDev;
    stage = "test-infra";
    tags = ["skims-small"];
  };
in {
  pipelines = {
    skims = {
      gitlabPath = "/skims/gitlab-ci.yaml";
      jobs =
        [
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
            output = "/lintTerraform/skims";
            gitlabExtra = gitlabLint;
          }
        ]
        ++ (builtins.map
          (category: {
            output = "/testPython/skims@${category}";
            gitDepth =
              if category == "unittesting"
              then 0
              else 1;
            gitlabExtra =
              gitlabTest
              // {
                after_script = ["cp ~/.makes/provenance-* ."];
                artifacts = {
                  name = "coverage_xml_$CI_COMMIT_REF_NAME_$CI_COMMIT_SHA";
                  paths = [
                    "skims/.coverage*"
                    "provenance-*"
                  ];
                  expire_in = "1 week";
                };
              };
          })
          inputs.skimsTestPythonCategoriesCI)
        ++ [
          {
            output = "/skims/coverage";
            gitlabExtra =
              gitlabTest
              // {
                needs =
                  builtins.map
                  (category: "/testPython/skims@${category}")
                  inputs.skimsTestPythonCategoriesCI;
                stage = "post-deploy";
              };
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
