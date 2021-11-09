{ gitlabCi
, ...
}:
let
  gitlabBranchNotMaster = gitlabCi.rules.branchNot "master";
  gitlabBranchMaster = gitlabCi.rules.branch "master";

  gitlabTitleMatchingMakes = gitlabCi.rules.titleMatching "^(all|integrates)";

  gitlabOnlyMaster = [
    gitlabBranchMaster
    gitlabCi.rules.notSchedules
    gitlabCi.rules.notTriggers
    gitlabTitleMatchingMakes
  ];
  gitlabOnlyDev = [
    gitlabBranchNotMaster
    gitlabCi.rules.notMrs
    gitlabCi.rules.notSchedules
    gitlabCi.rules.notTriggers
    gitlabTitleMatchingMakes
  ];

  gitlabDeployAppDev = {
    rules = gitlabOnlyDev;
    stage = "deploy-app";
    tags = [ "autoscaling" ];
  };
  gitlabDeployAppMaster = {
    rules = gitlabOnlyMaster;
    stage = "deploy-app";
    tags = [ "autoscaling" ];
  };
  gitlabDeployAppMasterResourceGroup = {
    resource_group = "deploy/$CI_JOB_NAME";
    rules = gitlabOnlyMaster;
    stage = "deploy-app";
    tags = [ "autoscaling" ];
  };
  gitlabDeployInfra = {
    resource_group = "deploy/$CI_JOB_NAME";
    rules = gitlabOnlyMaster;
    stage = "deploy-infra";
    tags = [ "autoscaling" ];
  };
  gitlabLint = {
    rules = gitlabOnlyDev;
    stage = "lint-code";
    tags = [ "autoscaling" ];
  };
  gitlabPostDeployDev = {
    rules = gitlabOnlyDev;
    stage = "post-deploy";
    tags = [ "autoscaling" ];
  };
  gitlabPreBuildDev = {
    rules = gitlabOnlyDev;
    stage = "pre-build";
    tags = [ "autoscaling" ];
  };
  gitlabPreBuildProd = {
    rules = gitlabOnlyMaster;
    stage = "pre-build";
    tags = [ "autoscaling" ];
  };
  gitlabTest = {
    rules = gitlabOnlyDev;
    stage = "test-code";
    tags = [ "autoscaling" ];
  };
  gitlabTestInfra = {
    rules = gitlabOnlyDev;
    stage = "test-infra";
    tags = [ "autoscaling" ];
  };

  chartsTemplate = {
    artifacts = {
      expire_in = "1 week";
      paths = [ "integrates/charts" ];
      when = "on_success";
    };
    stage = "analytics";
    tags = [ "autoscaling" ];
  };
  schedulerTemplate = {
    interruptible = false;
    stage = "scheduler";
  };
in
{
  pipelines = {
    integrates = {
      gitlabPath = "/makes/foss/modules/integrates/gitlab-ci.yaml";
      jobs = [ ]
        ++ (builtins.map
        (name: {
          args = [ "prod" "schedulers.${name}.main" ];
          output = "/computeOnAwsBatch/integratesScheduler";
          gitlabExtra = schedulerTemplate // {
            rules = [
              (gitlabCi.rules.schedules)
              (gitlabCi.rules.varIsDefined "integrates_scheduler_${name}")
              (gitlabCi.rules.always)
            ];
            tags = [ "autoscaling" ];
          };
        })
        [
          "update_indicators"
        ])
        ++ [
        {
          args = [ "prod" ];
          output = "/computeOnAwsBatch/integratesSubscriptionsUserToEntity";
          gitlabExtra = {
            interruptible = false;
            retry = 2;
            rules = [
              (gitlabCi.rules.schedules)
              (gitlabCi.rules.varIsDefined
                "integrates_subscriptions_trigger_user_to_entity_report_on_aws_prod_schedule")
              (gitlabCi.rules.always)
            ];
            stage = "subscriptions";
            tags = [ "autoscaling" ];
          };
        }
        {
          output = "/deployTerraform/integratesBackups";
          gitlabExtra = gitlabDeployInfra;
        }
        {
          output = "/deployTerraform/integratesCache";
          gitlabExtra = gitlabDeployInfra;
        }
        {
          output = "/deployTerraform/integratesDatabase";
          gitlabExtra = gitlabDeployInfra;
        }
        {
          output = "/deployTerraform/integratesFront";
          gitlabExtra = gitlabDeployInfra;
        }
        {
          output = "/deployTerraform/integratesResources";
          gitlabExtra = gitlabDeployInfra;
        }
        {
          output = "/deployTerraform/integratesSecrets";
          gitlabExtra = gitlabDeployInfra;
        }
        {
          output = "/integrates/back/authz-matrix";
          gitlabExtra = gitlabDeployAppDev;
        }
        {
          output = "/integrates/back/deploy/dev";
          gitlabExtra = gitlabDeployAppDev // {
            environment = {
              name = "development/$CI_COMMIT_REF_SLUG";
              url = "https://$CI_COMMIT_REF_SLUG.app.fluidattacks.com";
            };
          };
        }
        {
          output = "/integrates/back/deploy/prod";
          gitlabExtra = gitlabDeployAppMasterResourceGroup // {
            environment = {
              name = "production";
              url = "https://app.fluidattacks.com";
            };
          };
        }
        {
          args = [ "even" ];
          output = "/integrates/back/deploy/prod";
          gitlabExtra = gitlabDeployAppMaster // {
            environment = {
              name = "production";
              url = "https://app.fluidattacks.com";
            };
            needs = [ "/taintTerraform/makesUsersProdIntegratesKeys1" ];
            rules = [
              (gitlabCi.rules.schedules)
              (gitlabCi.rules.varIsDefined "makes_users_rotate_even")
              (gitlabCi.rules.always)
            ];
          };
        }
        {
          args = [ "odd" ];
          output = "/integrates/back/deploy/prod";
          gitlabExtra = gitlabDeployAppMaster // {
            environment = {
              name = "production";
              url = "https://app.fluidattacks.com";
            };
            needs = [ "/taintTerraform/makesUsersProdIntegratesKeys2" ];
            rules = [
              (gitlabCi.rules.schedules)
              (gitlabCi.rules.varIsDefined "makes_users_rotate_odd")
              (gitlabCi.rules.always)
            ];
          };
        }
        {
          output = "/integrates/back/destroy/eph";
          gitlabExtra = {
            rules = [
              (gitlabCi.rules.schedules)
              (gitlabCi.rules.varIsDefined "integrates_nightly_build")
              (gitlabCi.rules.always)
            ];
            stage = "rotation";
            tags = [ "autoscaling" ];
          };
        }
      ]
        ++ (builtins.map
        (args: {
          inherit args;
          output = "/integrates/back/test/functional";
          gitlabExtra = gitlabTest;
        })
        [
          [ "accept_legal" ]
          [ "acknowledge_concurrent_session" ]
          [ "activate_root" ]
          [ "add_draft" ]
          [ "add_event" ]
          [ "add_event_consult" ]
          [ "add_files_to_db" ]
          [ "add_finding_consult" ]
          [ "add_forces_execution" ]
          [ "add_git_root" ]
          [ "add_group" ]
          [ "add_group_consult" ]
          [ "add_group_tags" ]
          [ "add_organization" ]
          [ "add_push_token" ]
          [ "approve_draft" ]
          [ "confirm_vulnerabilities_zero_risk" ]
          [ "deactivate_root" ]
          [ "delete_obsolete_groups" ]
          [ "download_event_file" ]
          [ "download_file" ]
          [ "download_vulnerability_file" ]
          [ "event" ]
          [ "events" ]
          [ "finding" ]
          [ "forces_executions" ]
          [ "grant_stakeholder_access" ]
          [ "grant_stakeholder_organization_access" ]
          [ "group" ]
          [ "groups_with_forces" ]
          [ "handle_vulnerabilities_acceptance" ]
          [ "internal_names" ]
          [ "invalidate_access_token" ]
          [ "me" ]
          [ "organization" ]
          [ "organization_id" ]
          [ "reject_draft" ]
          [ "reject_vulnerabilities_zero_risk" ]
          [ "remove_event_evidence" ]
          [ "remove_evidence" ]
          [ "remove_files" ]
          [ "remove_finding" ]
          [ "remove_group" ]
          [ "remove_group_tag" ]
          [ "remove_stakeholder" ]
          [ "remove_stakeholder_access" ]
          [ "remove_stakeholder_organization_access" ]
          [ "remove_tags" ]
          [ "remove_vulnerability" ]
          [ "report" ]
          [ "request_vulnerabilities_verification" ]
          [ "request_vulnerabilities_zero_risk" ]
          [ "reset_expired_accepted_findings" ]
          [ "resources" ]
          [ "services_toe_lines" ]
          [ "sign_in" ]
          [ "solve_event" ]
          [ "stakeholder" ]
          [ "submit_draft" ]
          [ "submit_organization_finding_policy" ]
          [ "subscribe_to_entity_report" ]
          [ "toe_inputs" ]
          [ "toe_lines" ]
          [ "unsubscribe_from_group" ]
          [ "update_access_token" ]
          [ "update_event_evidence" ]
          [ "update_evidence_description" ]
          [ "update_evidence" ]
          [ "update_finding_description" ]
          [ "update_finding_description" ]
          [ "update_forces_access_token" ]
          [ "update_group" ]
          [ "update_group_info" ]
          [ "update_group_stakeholder" ]
          [ "update_organization_policies" ]
          [ "update_organization_stakeholder" ]
          [ "update_severity" ]
          [ "update_toe_lines_sorts" ]
          [ "update_vulnerabilities_treatment" ]
          [ "update_vulnerability_commit" ]
          [ "update_vulnerability_treatment" ]
          [ "upload_file" ]
          [ "verify_vulnerabilities_request" ]
          [ "vulnerability" ]
        ])
        ++ [
        {
          output = "/integrates/back/test/unit";
          gitlabExtra = gitlabTest // {
            artifacts = {
              name = "coverage_xml_$CI_COMMIT_REF_NAME_$CI_COMMIT_SHA";
              paths = [ "integrates/coverage.xml" ];
              expire_in = "1 week";
            };
          };
        }
        {
          args = [ "dev" ];
          output = "/integrates/charts/documents";
          gitlabExtra = chartsTemplate // {
            parallel = 6;
            rules = gitlabOnlyDev;
          };
        }
        {
          args = [ "prod" ];
          output = "/integrates/charts/documents";
          gitlabExtra = chartsTemplate // {
            interruptible = false;
            parallel = 15;
            rules = [
              (gitlabCi.rules.schedules)
              (gitlabCi.rules.varIsDefined "integrates_charts_make_documents_prod_schedule")
              (gitlabCi.rules.always)
            ];
          };
        }
        {
          args = [ "prod" ];
          output = "/integrates/charts/snapshots";
          gitlabExtra = {
            interruptible = false;
            rules = [
              (gitlabCi.rules.schedules)
              (gitlabCi.rules.varIsDefined "charts")
              (gitlabCi.rules.always)
            ];
            needs = [ "/integrates/charts/documents__prod" ];
            stage = "analytics";
            tags = [ "autoscaling" ];
          };
        }
        {
          output = "/integrates/coverage";
          gitlabExtra = {
            needs = [
              "/integrates/back/test/unit"
              "/integrates/front/test"
              "/integrates/mobile/test"
            ];
            rules = gitlabOnlyDev;
            stage = "external";
            tags = [ "autoscaling" ];
          };
        }
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
          gitlabExtra = gitlabTest // {
            after_script = [
              "cp ~/.makes/out-integrates-front-test/coverage/lcov.info integrates/front/coverage.lcov"
            ];
            artifacts = {
              expire_in = "1 week";
              name = "coverage_lcov_$CI_COMMIT_REF_NAME_$CI_COMMIT_SHORT_SHA";
              paths = [ "integrates/front/coverage.lcov" ];
            };
          };
        }
        {
          output = "/integrates/linters/back/schema";
          gitlabExtra = gitlabLint;
        }
        {
          output = "/integrates/linters/charts";
          gitlabExtra = gitlabLint;
        }
        {
          output = "/integrates/mobile/build/android";
          gitlabExtra = {
            artifacts = {
              expire_in = "1 day";
              paths = [ "integrates/mobile/output/" ];
              when = "on_success";
            };
            rules = gitlabOnlyMaster;
            stage = "build";
            tags = [ "autoscaling-large" ];
            needs = [ "/integrates/mobile/ota__prod" ];
            variables = {
              GIT_DEPTH = 5;
            };
          };
        }
        {
          output = "/integrates/mobile/deploy/playstore";
          gitlabExtra = {
            dependencies = [ "/integrates/mobile/build/android" ];
            rules = gitlabOnlyMaster;
            stage = "deploy-app";
            tags = [ "autoscaling" ];
            needs = [ "/integrates/mobile/build/android" ];
            variables = {
              GIT_DEPTH = 5;
            };
          };
        }
        {
          output = "/integrates/mobile/lint";
          gitlabExtra = gitlabLint;
        }
        {
          args = [ "dev" ];
          output = "/integrates/mobile/ota";
          gitlabExtra = gitlabPreBuildDev;
        }
        {
          args = [ "prod" ];
          output = "/integrates/mobile/ota";
          gitlabExtra = gitlabPreBuildProd;
        }
        {
          output = "/integrates/mobile/test";
          gitlabExtra = gitlabTest // {
            after_script = [
              "cp ~/.makes/out-integrates-mobile-test/coverage/lcov.info integrates/mobile/coverage.lcov"
            ];
            artifacts = {
              expire_in = "1 week";
              name = "coverage_lcov_$CI_COMMIT_REF_NAME_$CI_COMMIT_SHORT_SHA";
              paths = [ "integrates/mobile/coverage.lcov" ];
            };
          };
        }
      ]
        ++ (builtins.map
        (name: {
          args = [ "prod" "schedulers.${name}.main" ];
          output = "/integrates/scheduler";
          gitlabExtra = schedulerTemplate // {
            rules = [
              (gitlabCi.rules.schedules)
              (gitlabCi.rules.varIsDefined "integrates_scheduler_${name}")
              (gitlabCi.rules.always)
            ];
            tags = [ "autoscaling-large" ];
          };
        })
        [
          "delete_imamura_stakeholders"
          "delete_obsolete_groups"
          "delete_obsolete_orgs"
          "get_remediated_findings"
          "reset_expired_accepted_findings"
          "update_portfolios"
          "requeue_actions"
          "machine_queue_all"
          "machine_queue_re_attacks"
          "send_treatment_change"
          "toe_inputs_etl"
          "services_toe_lines_etl"
        ])
        ++ [
        {
          output = "/integrates/secrets/lint";
          gitlabExtra = gitlabLint;
        }
        {
          args = [ "dev" ];
          output = "/integrates/subscriptions/user-to-entity";
          gitlabExtra = {
            retry = 2;
            rules = gitlabOnlyDev;
            stage = "subscriptions";
            tags = [ "autoscaling" ];
          };
        }
        {
          output = "/integrates/web/e2e";
          gitlabExtra = gitlabPostDeployDev // {
            needs = [
              "/integrates/back/deploy/dev"
              "/integrates/front/deploy/dev"
            ];
            parallel = 5;
            retry = 2;
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
          output = "/lintPython/module/integratesBackMigrations";
          gitlabExtra = gitlabLint;
        }
        # TODO: https://gitlab.com/fluidattacks/product/-/issues/5246
        # {
        #   output = "/lintPython/module/integratesBackTests";
        #   gitlabExtra = gitlabLint;
        # }
        {
          output = "/lintPython/module/integratesBackTestsE2e";
          gitlabExtra = gitlabLint;
        }
        {
          output = "/lintTerraform/integratesBackups";
          gitlabExtra = gitlabLint;
        }
        {
          output = "/lintTerraform/integratesCache";
          gitlabExtra = gitlabLint;
        }
        {
          output = "/lintTerraform/integratesDatabase";
          gitlabExtra = gitlabLint;
        }
        {
          output = "/lintTerraform/integratesFront";
          gitlabExtra = gitlabLint;
        }
        {
          output = "/lintTerraform/integratesResources";
          gitlabExtra = gitlabLint;
        }
        {
          output = "/lintTerraform/integratesSecrets";
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
          output = "/testTerraform/integratesBackups";
          gitlabExtra = gitlabTestInfra;
        }
        {
          output = "/testTerraform/integratesCache";
          gitlabExtra = gitlabTestInfra;
        }
        {
          output = "/testTerraform/integratesDatabase";
          gitlabExtra = gitlabTestInfra;
        }
        {
          output = "/testTerraform/integratesFront";
          gitlabExtra = gitlabTestInfra;
        }
        {
          output = "/testTerraform/integratesResources";
          gitlabExtra = gitlabTestInfra;
        }
        {
          output = "/testTerraform/integratesSecrets";
          gitlabExtra = gitlabTestInfra;
        }
      ];
    };
  };
}
