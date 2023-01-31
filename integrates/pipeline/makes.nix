{
  gitlabCi,
  inputs,
  lib,
  projectPath,
  ...
}: let
  chartsTemplate = {
    after_script = ["cp ~/.makes/provenance-* ."];
    artifacts = {
      expire_in = "1 week";
      paths = [
        "integrates/charts"
        "provenance-*"
      ];
      when = "on_success";
    };
    stage = "analytics";
  };
  listDirectories = path: let
    content = builtins.readDir (projectPath path);
    directories =
      lib.filterAttrs
      (key: value: value == "directory" && !lib.hasPrefix "__" key)
      content;
  in
    builtins.attrNames directories;
  backSrcModules = listDirectories "/integrates/back/src";
  functionalTests =
    builtins.map (test: [test])
    (listDirectories "/integrates/back/test/functional/src");
  gitlabJobDependencies = 40;
  functionalCoverageCombine = (
    builtins.genList
    (x: [(builtins.toString (x + 1))])
    (
      builtins.ceil
      ((builtins.length functionalTests) / (gitlabJobDependencies * 1.0))
    )
  );
  gitlabBranchNotTrunk = gitlabCi.rules.branchNot "trunk";
  gitlabBranchTrunk = gitlabCi.rules.branch "trunk";
  gitlabTitleMatchingMakes = gitlabCi.rules.titleMatching "^(all|integrates)";
  gitlabOnlyProd = [
    gitlabBranchTrunk
    gitlabCi.rules.notSchedules
    gitlabCi.rules.notTriggers
    gitlabTitleMatchingMakes
  ];
  gitlabOnlyDev = [
    gitlabBranchNotTrunk
    gitlabCi.rules.notMrs
    gitlabCi.rules.notSchedules
    gitlabCi.rules.notTriggers
    gitlabTitleMatchingMakes
  ];
  gitlabOnlyDevAndProd = [
    gitlabCi.rules.notMrs
    gitlabCi.rules.notSchedules
    gitlabCi.rules.notTriggers
    gitlabTitleMatchingMakes
  ];
  gitlabDeployEphemeralRule = [
    gitlabCi.rules.notMrs
    gitlabCi.rules.notSchedules
    gitlabCi.rules.notTriggers
    # Integrates and forces only need ephemeral in dev
    gitlabBranchNotTrunk
    (gitlabCi.rules.titleMatching "^(all|integrates)")
  ];
  gitlabDeployAppDev = {
    rules = gitlabOnlyDev;
    stage = "deploy-app";
    tags = ["small"];
  };
  gitlabDeployAppDevInterested = {
    rules = gitlabDeployEphemeralRule;
    stage = "deploy-app";
    tags = ["small"];
  };
  gitlabDeployAppProdResourceGroup = {
    resource_group = "deploy/$CI_JOB_NAME";
    rules = gitlabOnlyProd;
    stage = "deploy-app";
    tags = ["small"];
  };
  gitlabDeployForcesProd = {
    rules = gitlabOnlyProd;
    stage = "deploy-app";
    tags = ["small"];
  };
  gitlabDeployInfra = {
    resource_group = "deploy/$CI_JOB_NAME";
    rules = gitlabOnlyProd;
    stage = "deploy-infra";
    tags = ["small"];
  };
  gitlabExternal = {
    rules = gitlabOnlyDevAndProd;
    stage = "external";
    tags = ["small"];
  };
  gitlabLint = {
    rules = gitlabOnlyDev;
    stage = "lint-code";
    tags = ["small"];
  };
  gitlabPostDeployDev = {
    rules = gitlabOnlyDev;
    stage = "post-deploy";
    tags = ["small"];
  };
  gitlabTestDevAndProd = {
    rules = gitlabOnlyDevAndProd;
    stage = "test-code";
    tags = ["small"];
  };
  gitlabTestInfra = {
    rules = gitlabOnlyDev;
    stage = "test-infra";
    tags = ["small"];
  };
  lib = inputs.nixpkgs.lib;
in {
  pipelines = {
    integrates = {
      gitlabPath = "/integrates/gitlab-ci.yaml";
      jobs =
        []
        ++ [
          {
            output = "/deployTerraform/integratesInfra";
            gitlabExtra = gitlabDeployInfra;
          }
          {
            output = "/integrates/back/authz-matrix";
            gitlabExtra =
              gitlabDeployAppDev
              // {
                after_script = ["cp ~/.makes/provenance-* ."];
                artifacts = {
                  paths = [
                    "integrates/back/deploy/permissions_matrix"
                    "provenance-*"
                  ];
                  expire_in = "1 day";
                  when = "on_success";
                };
              };
          }
          {
            output = "/deployContainerImage/forcesDev";
            gitlabExtra = gitlabDeployAppDevInterested;
          }
          {
            output = "/deployContainerImage/forcesProd";
            gitlabExtra = gitlabDeployForcesProd;
          }
          {
            output = "/integrates/back/deploy/dev";
            gitlabExtra =
              gitlabDeployAppDevInterested
              // {
                environment = {
                  name = "development/$CI_COMMIT_REF_SLUG";
                  url = "https://$CI_COMMIT_REF_SLUG.app.fluidattacks.com";
                };
              };
          }
          {
            output = "/integrates/back/deploy/prod";
            gitlabExtra =
              gitlabDeployAppProdResourceGroup
              // {
                environment = {
                  name = "production";
                  url = "https://app.fluidattacks.com";
                };
              };
          }
        ]
        ++ (builtins.map
          (args: {
            inherit args;
            output = "/integrates/back/test/functional";
            gitlabExtra =
              gitlabTestDevAndProd
              // {
                after_script = ["cp ~/.makes/provenance-* ."];
                artifacts = {
                  paths = [
                    "integrates/.coverage*"
                    "provenance-*"
                  ];
                  expire_in = "1 day";
                  when = "on_success";
                };
                variables = {
                  MAKES_NON_ROOT = 1;
                };
              };
          })
          functionalTests)
        ++ [
          {
            output = "/forces/test";
            gitlabExtra =
              gitlabTestDevAndProd
              // {
                variables = {
                  MAKES_NON_ROOT = 1;
                };
              };
          }
          {
            args = ["changes_db"];
            output = "/integrates/back/test/unit";
            gitlabExtra =
              gitlabTestDevAndProd
              // {
                after_script = ["cp ~/.makes/provenance-* ."];
                artifacts = {
                  name = "coverage_xml_$CI_COMMIT_REF_NAME_$CI_COMMIT_SHA";
                  paths = [
                    "integrates/.coverage*"
                    "provenance-*"
                  ];
                  expire_in = "1 week";
                };
                variables = {
                  MAKES_NON_ROOT = 1;
                };
              };
          }
          {
            args = ["not_changes_db"];
            output = "/integrates/back/test/unit";
            gitlabExtra =
              gitlabTestDevAndProd
              // {
                after_script = ["cp ~/.makes/provenance-* ."];
                artifacts = {
                  name = "coverage_xml_$CI_COMMIT_REF_NAME_$CI_COMMIT_SHA";
                  paths = [
                    "integrates/.coverage*"
                    "provenance-*"
                  ];
                  expire_in = "1 week";
                };
                variables = {
                  MAKES_NON_ROOT = 1;
                };
              };
          }
          rec {
            args = ["dev" (toString gitlabExtra.parallel) "gitlab"];
            output = "/integrates/charts/documents";
            gitlabExtra =
              chartsTemplate
              // {
                parallel = 7;
                rules = gitlabOnlyDev;
                tags = ["small"];
                variables = {
                  MAKES_NON_ROOT = 1;
                };
              };
          }
          rec {
            args = ["prod" (toString gitlabExtra.parallel) "gitlab"];
            output = "/integrates/charts/documents";
            gitlabExtra =
              chartsTemplate
              // {
                interruptible = false;
                parallel = 30;
                rules = [
                  (gitlabCi.rules.schedules)
                  (
                    gitlabCi.rules.varIsDefined
                    "integrates_charts_make_documents_prod_schedule"
                  )
                  (gitlabCi.rules.always)
                ];
                tags = ["small"];
              };
          }
          {
            args = ["prod"];
            output = "/integrates/charts/snapshots";
            gitlabExtra = {
              interruptible = false;
              rules = [
                (gitlabCi.rules.schedules)
                (gitlabCi.rules.varIsDefined "charts")
                (gitlabCi.rules.always)
              ];
              needs = ["/integrates/charts/documents__prod__30__gitlab"];
              stage = "analytics";
              tags = ["small"];
              variables = {
                MAKES_NON_ROOT = 1;
              };
            };
          }
          {
            output = "/integrates/coverage";
            gitlabExtra =
              gitlabExternal
              // {
                after_script = ["cp ~/.makes/provenance-* ."];
                artifacts = {
                  paths = [
                    "integrates/build"
                    "provenance-*"
                  ];
                  expire_in = "1 day";
                  when = "on_success";
                  reports = {
                    coverage_report = {
                      coverage_format = "cobertura";
                      path = "integrates/coverage.xml";
                    };
                  };
                };
                coverage = "/(?i)total.*? (100(?:\\.0+)?\\%|[1-9]?\\d(?:\\.\\d+)?\\%)$/";
                needs =
                  [
                    "/integrates/back/test/unit__changes_db"
                    "/integrates/back/test/unit__not_changes_db"
                  ]
                  ++ (
                    builtins.map
                    (test: "/integrates/coverage/combine__${
                      builtins.elemAt
                      test
                      0
                    }")
                    functionalCoverageCombine
                  );
              };
          }
        ]
        ++ (builtins.map
          (args: {
            inherit args;
            output = "/integrates/coverage/combine";
            gitlabExtra =
              gitlabExternal
              // {
                after_script = ["cp ~/.makes/provenance-* ."];
                artifacts = {
                  paths = [
                    "integrates/.coverage*"
                    "provenance-*"
                  ];
                  expire_in = "1 day";
                  when = "on_success";
                };
                needs = (
                  builtins.map
                  (test: "/integrates/back/test/functional__${
                    builtins.elemAt
                    test
                    0
                  }")
                  (
                    lib.lists.sublist
                    (
                      (
                        (
                          lib.strings.toInt
                          (builtins.elemAt args 0)
                        )
                        - 1
                      )
                      * gitlabJobDependencies
                    )
                    gitlabJobDependencies
                    functionalTests
                  )
                );
              };
          })
          functionalCoverageCombine)
        ++ [
          {
            output = "/integrates/front/deploy/dev";
            gitlabExtra = gitlabDeployAppDev;
          }
          {
            output = "/integrates/front/deploy/prod";
            gitlabExtra = gitlabDeployAppProdResourceGroup;
          }
          {
            output = "/integrates/front/lint";
            gitlabExtra = gitlabLint;
          }
          {
            output = "/integrates/front/test";
            gitlabExtra =
              gitlabTestDevAndProd
              // {
                parallel = 5;
              };
          }
          {
            output = "/integrates/back/lint/schema";
            gitlabExtra = gitlabLint // {allow_failure = true;};
          }
          {
            output = "/integrates/back/lint/schema/deprecations";
            gitlabExtra = gitlabLint;
          }
          {
            output = "/integrates/back/lint/charts";
            gitlabExtra = gitlabLint;
          }
        ]
        ++ (builtins.map
          (frequency: {
            args = ["dev" frequency];
            output = "/integrates/subscriptions/analytics";
            gitlabExtra = {
              retry = 2;
              rules = gitlabOnlyDev;
              stage = "subscriptions";
              tags = ["small"];
              variables = {
                MAKES_NON_ROOT = 1;
              };
            };
          })
          [
            "daily"
            "hourly"
            "monthly"
            "weekly"
          ])
        ++ [
          {
            output = "/integrates/secrets/lint";
            gitlabExtra = gitlabLint;
          }
          {
            output = "/integrates/web/e2e";
            gitlabExtra =
              gitlabPostDeployDev
              // {
                needs = [
                  "/integrates/back/deploy/dev"
                  "/integrates/front/deploy/dev"
                ];
                parallel = 5;
                retry = 2;
              };
          }
          {
            output = "/integrates/web/forces";
            gitlabExtra =
              gitlabPostDeployDev
              // {
                needs = [
                  "/integrates/back/deploy/dev"
                ];
                retry = 2;
              };
          }
        ]
        ++ (builtins.map
          (module: {
            output = "/lintPython/dirOfModules/integrates/${module}";
            gitlabExtra = gitlabLint;
          })
          backSrcModules)
        ++ [
          {
            output = "/lintPython/module/integratesBackCharts";
            gitlabExtra = gitlabLint;
          }
          {
            output = "/lintPython/module/integratesBackChartsCollector";
            gitlabExtra = gitlabLint;
          }
          {
            output = "/lintPython/dirOfModules/integratesBackChartsGenerators";
            gitlabExtra = gitlabLint;
          }
          {
            output = "/lintPython/dirOfModules/streams";
            gitlabExtra = gitlabLint;
          }
          {
            output = "/lintPython/imports/integrates";
            gitlabExtra = gitlabLint;
          }
          {
            output = "/lintPython/module/integratesBackDeployPermissionsMatrix";
            gitlabExtra = gitlabLint;
          }
          {
            output = "/lintPython/module/integratesJobsCloneRoots";
            gitlabExtra = gitlabLint;
          }
          {
            output = "/lintPython/module/integratesJobsExecuteMachine";
            gitlabExtra = gitlabLint;
          }
          {
            output = "/lintPython/module/integratesBackMigrations";
            gitlabExtra = gitlabLint;
          }
          {
            output = "/lintPython/module/integratesBackTest";
            gitlabExtra = gitlabLint;
          }
          {
            output = "/lintPython/module/integratesBackTestE2e";
            gitlabExtra = gitlabLint;
          }
          {
            output = "/lintPython/module/forces";
            gitlabExtra = gitlabLint;
          }
          {
            output = "/lintPython/module/forcesTests";
            gitlabExtra = gitlabLint;
          }
          {
            output = "/lintTerraform/integratesInfra";
            gitlabExtra = gitlabLint;
          }
          {
            output = "/pipelineOnGitlab/integrates";
            gitlabExtra = gitlabLint;
          }
          {
            output = "/securePythonWithBandit/integratesBack";
            gitlabExtra = gitlabLint;
          }
          {
            output = "/testTerraform/integratesInfra";
            gitlabExtra = gitlabTestInfra;
          }
        ];
    };
  };
}
