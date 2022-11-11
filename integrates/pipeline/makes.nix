# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0
{
  gitlabCi,
  inputs,
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
  backSrcModules = [
    "analytics"
    "api"
    "app"
    "authz"
    "azure_repositories"
    "batch"
    "batch_dispatch"
    "billing"
    "cli"
    "context"
    "custom_exceptions"
    "dataloaders"
    "db_model"
    "decorators"
    "dynamodb"
    "enrollment"
    "event_comments"
    "events"
    "finding_comments"
    "findings"
    "forces"
    "group_access"
    "group_comments"
    "groups"
    "machine"
    "mailer"
    "newutils"
    "notifications"
    "organizations"
    "organizations_finding_policies"
    "redshift"
    "remove_stakeholder"
    "reports"
    "roots"
    "s3"
    "schedulers"
    "search"
    "server"
    "sessions"
    "settings"
    "sms"
    "stakeholders"
    "subscriptions"
    "tags"
    "telemetry"
    "toe"
    "unreliable_indicators"
    "verify"
    "vulnerabilities"
    "vulnerability_files"
  ];
  functionalTests = [
    ["abandoned_trial_notification"]
    ["accept_legal"]
    ["acknowledge_concurrent_session"]
    ["activate_root"]
    ["add_credentials"]
    ["add_draft"]
    ["add_enrollment"]
    ["add_event"]
    ["add_event_consult"]
    ["add_files_to_db"]
    ["add_finding_consult"]
    ["add_forces_execution_s3"]
    ["add_git_root_s3"]
    ["add_group"]
    ["add_group_consult"]
    ["add_group_tags"]
    ["add_organization"]
    ["add_stakeholder"]
    ["add_toe_input"]
    ["add_toe_lines"]
    ["add_url_root"]
    ["approve_draft"]
    ["batch"]
    ["batch_dispatch_s3"]
    ["compliance"]
    ["confirm_vulnerabilities_zero_risk"]
    ["deactivate_root"]
    ["delete_obsolete_groups"]
    ["download_event_file"]
    ["download_file"]
    ["download_vulnerability_file_s3"]
    ["event"]
    ["events"]
    ["expire_free_trial"]
    ["finding"]
    ["forces_executions_s3"]
    ["grant_stakeholder_access"]
    ["grant_stakeholder_organization_access"]
    ["group_s3"]
    ["groups_languages_distribution"]
    ["groups_with_forces"]
    ["handle_vulnerabilities_acceptance"]
    ["invalidate_access_token"]
    ["machine_queue_all"]
    ["me"]
    ["move_root"]
    ["organization"]
    ["organization_id"]
    ["organization_vulnerabilities"]
    ["refresh_toe_inputs"]
    ["refresh_toe_lines"]
    ["reject_draft"]
    ["reject_event_solution"]
    ["reject_vulnerabilities_zero_risk"]
    ["remove_credentials"]
    ["remove_event_evidence_s3"]
    ["remove_evidence_s3"]
    ["remove_files_s3"]
    ["remove_finding_s3"]
    ["remove_group_s3"]
    ["remove_group_tag"]
    ["remove_stakeholder"]
    ["remove_stakeholder_access"]
    ["remove_stakeholder_organization_access"]
    ["remove_tags"]
    ["remove_vulnerability"]
    ["report"]
    ["request_event_verification"]
    ["request_vulnerabilities_hold"]
    ["request_vulnerabilities_verification"]
    ["request_vulnerabilities_zero_risk"]
    ["requeue_actions"]
    ["report_machine_s3"]
    ["reset_expired_accepted_findings"]
    ["resources"]
    ["solve_event"]
    ["stakeholder"]
    ["submit_draft"]
    ["submit_organization_finding_policy"]
    ["subscribe_to_entity_report_s3"]
    ["sync_git_root_s3"]
    ["toe_inputs"]
    ["toe_lines"]
    ["unfulfilled_standard_report_url_s3"]
    ["unsubscribe_from_group"]
    ["update_access_token"]
    ["update_compliance"]
    ["update_credentials"]
    ["update_event"]
    ["update_event_evidence_s3"]
    ["update_event_solving_reason"]
    ["update_evidence_description"]
    ["update_evidence_s3"]
    ["update_finding_description"]
    ["update_forces_access_token"]
    ["update_git_environments"]
    ["update_git_root_s3"]
    ["update_group_s3"]
    ["update_group_access_info"]
    ["update_group_disambiguation"]
    ["update_group_info"]
    ["update_group_managed"]
    ["update_group_policies"]
    ["update_group_stakeholder"]
    ["update_ip_root"]
    ["update_notification_preferences"]
    ["update_organization_policies"]
    ["update_organization_stakeholder"]
    ["update_severity"]
    ["update_stakeholder_phone"]
    ["update_toe_input"]
    ["update_toe_lines_attacked_lines"]
    ["update_toe_lines_sorts"]
    ["update_toe_vulnerabilities"]
    ["update_tours"]
    ["update_url_root"]
    ["update_vulnerabilities_treatment"]
    ["update_vulnerability_description"]
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
    (gitlabCi.rules.titleMatching "^(all|integrates|forces)")
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
  gitlabTestDev = {
    rules = gitlabOnlyDev;
    stage = "test-code";
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
            output = "/integrates/back/test/check-forces-output";
            gitlabExtra =
              gitlabTestDev
              // {
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
                after_script = [
                  "cp ~/.makes/out-integrates-front-test/coverage/lcov.info integrates/front/coverage.lcov"
                  "cp ~/.makes/provenance-* ."
                ];
                artifacts = {
                  expire_in = "1 week";
                  name = "coverage_lcov_$CI_COMMIT_REF_NAME_$CI_COMMIT_SHORT_SHA";
                  paths = [
                    "integrates/front/coverage.lcov"
                    "provenance-*"
                  ];
                };
              };
          }
          {
            output = "/integrates/back/lint/schema";
            gitlabExtra = gitlabLint;
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
            output = "/integrates/web/check-forces-output";
            gitlabExtra =
              gitlabPostDeployDev
              // {
                needs = [
                  "/integrates/back/deploy/dev"
                ];
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
