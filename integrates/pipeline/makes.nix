{
  gitlabCi,
  inputs,
  ...
}: let
  chartsTemplate = {
    artifacts = {
      expire_in = "1 week";
      paths = ["integrates/charts"];
      when = "on_success";
    };
    stage = "analytics";
    tags = ["autoscaling"];
  };
  functionalTests = [
    ["accept_legal"]
    ["acknowledge_concurrent_session"]
    ["activate_root"]
    ["add_credentials"]
    ["add_draft"]
    ["add_event"]
    ["add_event_consult"]
    ["add_files_to_db"]
    ["add_finding_consult"]
    ["add_forces_execution"]
    ["add_git_root"]
    ["add_group"]
    ["add_group_consult"]
    ["add_group_tags"]
    ["add_organization"]
    ["add_push_token"]
    ["add_toe_input"]
    ["add_toe_lines"]
    ["add_url_root"]
    ["approve_draft"]
    ["batch"]
    ["confirm_vulnerabilities_zero_risk"]
    ["deactivate_root"]
    ["delete_obsolete_groups"]
    ["download_event_file"]
    ["download_file"]
    ["download_vulnerability_file"]
    ["event"]
    ["events"]
    ["finding"]
    ["forces_executions"]
    ["grant_stakeholder_access"]
    ["grant_stakeholder_organization_access"]
    ["group"]
    ["groups_with_forces"]
    ["handle_vulnerabilities_acceptance"]
    ["invalidate_access_token"]
    ["me"]
    ["move_root"]
    ["organization"]
    ["organization_id"]
    ["refresh_toe_inputs"]
    ["refresh_toe_lines"]
    ["reject_draft"]
    ["reject_vulnerabilities_zero_risk"]
    ["remove_credentials"]
    ["remove_event_evidence"]
    ["remove_evidence"]
    ["remove_files"]
    ["remove_finding"]
    ["remove_group"]
    ["remove_group_tag"]
    ["remove_stakeholder"]
    ["remove_stakeholder_access"]
    ["remove_stakeholder_organization_access"]
    ["remove_tags"]
    ["remove_vulnerability"]
    ["report"]
    ["request_vulnerabilities_hold"]
    ["request_vulnerabilities_verification"]
    ["request_vulnerabilities_zero_risk"]
    ["requeue_actions"]
    ["reset_expired_accepted_findings"]
    ["resources"]
    ["sign_in"]
    ["solve_event"]
    ["stakeholder"]
    ["submit_draft"]
    ["submit_organization_finding_policy"]
    ["subscribe_to_entity_report"]
    ["sync_git_root"]
    ["toe_inputs"]
    ["toe_lines"]
    ["unsubscribe_from_group"]
    ["update_access_token"]
    ["update_credentials"]
    ["update_event_evidence"]
    ["update_event_solving_reason"]
    ["update_evidence_description"]
    ["update_evidence"]
    ["update_finding_description"]
    ["update_forces_access_token"]
    ["update_git_environments"]
    ["update_git_root"]
    ["update_group"]
    ["update_group_access_info"]
    ["update_group_disambiguation"]
    ["update_group_info"]
    ["update_group_managed"]
    ["update_group_policies"]
    ["update_group_stakeholder"]
    ["update_ip_root"]
    ["update_nickname"]
    ["update_organization_policies"]
    ["update_organization_stakeholder"]
    ["update_severity"]
    ["update_stakeholder_phone"]
    ["update_toe_input"]
    ["update_toe_lines_attacked_lines"]
    ["update_toe_lines_sorts"]
    ["update_url_root"]
    ["update_vulnerabilities_treatment"]
    ["update_vulnerability_commit"]
    ["update_vulnerability_treatment"]
    ["upload_file"]
    ["validate_git_access"]
    ["verify_stakeholder"]
    ["verify_vulnerabilities_request"]
    ["vulnerability"]
  ];
  gitlabJobDependencies = 40;
  functionalCoverageCombine = (
    builtins.genList
    (x: [(builtins.toString (x + 1))])
    ((
        builtins.floor
        ((builtins.length functionalTests) / gitlabJobDependencies)
      )
      + 1)
  );
  gitlabBranchNotTrunk = gitlabCi.rules.branchNot "trunk";
  gitlabBranchTrunk = gitlabCi.rules.branch "trunk";
  gitlabTitleMatchingMakes = gitlabCi.rules.titleMatching "^(all|integrates)";
  gitlabOnlyMaster = [
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
  gitlabDeployEphemeralRule = [
    gitlabBranchNotTrunk
    gitlabCi.rules.notMrs
    gitlabCi.rules.notSchedules
    gitlabCi.rules.notTriggers
    (gitlabCi.rules.titleMatching "^(all|integrates|skims|forces)")
  ];
  gitlabDeployAppDev = {
    rules = gitlabOnlyDev;
    stage = "deploy-app";
    tags = ["autoscaling"];
  };
  gitlabDeployAppDevInterested = {
    rules = gitlabDeployEphemeralRule;
    stage = "deploy-app";
    tags = ["autoscaling"];
  };
  gitlabDeployAppMaster = {
    rules = gitlabOnlyMaster;
    stage = "deploy-app";
    tags = ["autoscaling"];
  };
  gitlabDeployAppMasterResourceGroup = {
    resource_group = "deploy/$CI_JOB_NAME";
    rules = gitlabOnlyMaster;
    stage = "deploy-app";
    tags = ["autoscaling"];
  };
  gitlabDeployInfra = {
    resource_group = "deploy/$CI_JOB_NAME";
    rules = gitlabOnlyMaster;
    stage = "deploy-infra";
    tags = ["autoscaling"];
  };
  gitlabExternal = {
    rules = gitlabOnlyDev;
    stage = "external";
    tags = ["autoscaling"];
  };
  gitlabLint = {
    rules = gitlabOnlyDev;
    stage = "lint-code";
    tags = ["autoscaling"];
  };
  gitlabPostDeployDev = {
    rules = gitlabOnlyDev;
    stage = "post-deploy";
    tags = ["autoscaling"];
  };
  gitlabTest = {
    rules = gitlabOnlyDev;
    stage = "test-code";
    tags = ["autoscaling"];
  };
  gitlabTestInfra = {
    rules = gitlabOnlyDev;
    stage = "test-infra";
    tags = ["autoscaling"];
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
                artifacts = {
                  paths = ["integrates/back/deploy/permissions_matrix"];
                  expire_in = "1 day";
                  when = "on_success";
                };
              };
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
              gitlabDeployAppMasterResourceGroup
              // {
                environment = {
                  name = "production";
                  url = "https://app.fluidattacks.com";
                };
              };
          }
          {
            args = ["even"];
            output = "/integrates/back/deploy/prod";
            gitlabExtra =
              gitlabDeployAppMaster
              // {
                environment = {
                  name = "production";
                  url = "https://app.fluidattacks.com";
                };
                needs = ["/taintTerraform/commonUsersKeys1"];
                rules = [
                  (gitlabCi.rules.schedules)
                  (gitlabCi.rules.varIsDefined "common_users_rotate_even")
                  (gitlabCi.rules.always)
                ];
              };
          }
          {
            args = ["odd"];
            output = "/integrates/back/deploy/prod";
            gitlabExtra =
              gitlabDeployAppMaster
              // {
                environment = {
                  name = "production";
                  url = "https://app.fluidattacks.com";
                };
                needs = ["/taintTerraform/commonUsersKeys2"];
                rules = [
                  (gitlabCi.rules.schedules)
                  (gitlabCi.rules.varIsDefined "common_users_rotate_odd")
                  (gitlabCi.rules.always)
                ];
              };
          }
        ]
        ++ (builtins.map
          (args: {
            inherit args;
            output = "/integrates/back/test/functional";
            gitlabExtra =
              gitlabTest
              // {
                artifacts = {
                  paths = ["integrates/.coverage*"];
                  expire_in = "1 day";
                  when = "on_success";
                };
              };
          })
          functionalTests)
        ++ [
          {
            output = "/integrates/back/test/unit";
            gitlabExtra =
              gitlabTest
              // {
                artifacts = {
                  name = "coverage_xml_$CI_COMMIT_REF_NAME_$CI_COMMIT_SHA";
                  paths = [
                    "integrates/.coverage*"
                  ];
                  expire_in = "1 week";
                };
              };
          }
          {
            output = "/integrates/back/test/check-forces-output";
            gitlabExtra = gitlabTest;
          }
          rec {
            args = ["dev" (toString gitlabExtra.parallel) "gitlab"];
            output = "/integrates/charts/documents";
            gitlabExtra =
              chartsTemplate
              // {
                parallel = 7;
                rules = gitlabOnlyDev;
              };
          }
          rec {
            args = ["prod" (toString gitlabExtra.parallel) "gitlab"];
            output = "/integrates/charts/documents";
            gitlabExtra =
              chartsTemplate
              // {
                interruptible = false;
                parallel = 25;
                rules = [
                  (gitlabCi.rules.schedules)
                  (
                    gitlabCi.rules.varIsDefined
                    "integrates_charts_make_documents_prod_schedule"
                  )
                  (gitlabCi.rules.always)
                ];
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
              needs = ["/integrates/charts/documents__prod__25__gitlab"];
              stage = "analytics";
              tags = ["autoscaling"];
            };
          }
          {
            output = "/integrates/coverage";
            gitlabExtra =
              gitlabExternal
              // {
                artifacts = {
                  paths = ["integrates/build"];
                  expire_in = "1 day";
                  when = "on_success";
                };
                needs =
                  [
                    "/integrates/back/test/unit"
                    "/integrates/front/test"
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
                artifacts = {
                  paths = ["integrates/.coverage*"];
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
            gitlabExtra = gitlabDeployAppMasterResourceGroup;
          }
          {
            output = "/integrates/front/lint";
            gitlabExtra = gitlabLint;
          }
          {
            output = "/integrates/front/test";
            gitlabExtra =
              gitlabTest
              // {
                after_script = [
                  "cp ~/.makes/out-integrates-front-test/coverage/lcov.info integrates/front/coverage.lcov"
                ];
                artifacts = {
                  expire_in = "1 week";
                  name = "coverage_lcov_$CI_COMMIT_REF_NAME_$CI_COMMIT_SHORT_SHA";
                  paths = ["integrates/front/coverage.lcov"];
                };
              };
          }
          {
            output = "/integrates/back/lint/schema";
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
              tags = ["autoscaling"];
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
            output = "/integrates/web/check-forces-output";
            gitlabExtra =
              gitlabPostDeployDev
              // {
                needs = [
                  "/integrates/back/deploy/dev"
                ];
              };
          }
          {
            output = "/lintPython/dirOfModules/integrates";
            gitlabExtra = gitlabLint;
          }
          {
            output = "/lintPython/dirOfModules/integratesBackChartsGenerators";
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
