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
  gitlabPostDeployDev = {
    rules = gitlabOnlyDev;
    stage = "post-deploy";
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
in
{
  pipelines = {
    integrates = {
      gitlabPath = "/makes/foss/modules/integrates/gitlab-ci.yaml";
      jobs = [
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
          [ "add_draft_new" "false" "migration" ]
          [ "add_event" ]
          [ "add_event_consult" ]
          [ "add_files_to_db" ]
          [ "add_finding_consult" ]
          [ "add_finding_consult_new" "false" "migration" ]
          [ "add_forces_execution" ]
          [ "add_git_root" ]
          [ "add_group" ]
          [ "add_group_consult" ]
          [ "add_group_tags" ]
          [ "add_organization" ]
          [ "add_push_token" ]
          [ "approve_draft" ]
          [ "approve_draft_new" "false" "migration" ]
          [ "confirm_vulnerabilities_zero_risk" ]
          [ "deactivate_root" ]
          [ "delete_obsolete_groups_new" "false" "migration" ]
          [ "download_event_file" ]
          [ "download_file" ]
          [ "download_vulnerability_file" ]
          [ "download_vulnerability_file_new" "false" "migration" ]
          [ "event" ]
          [ "events" ]
          [ "finding" ]
          [ "finding_new" "false" "migration" ]
          [ "forces_executions" ]
          [ "grant_stakeholder_access" ]
          [ "grant_stakeholder_organization_access" ]
          [ "group" ]
          [ "group_new" "false" "migration" ]
          [ "groups_with_forces" ]
          [ "handle_vulnerabilities_acceptation_new" "false" "migration" ]
          [ "internal_names" ]
          [ "invalidate_access_token" ]
          [ "me" ]
          [ "old" "true" ]
          [ "organization" ]
          [ "organization_id" ]
          [ "reject_draft" ]
          [ "reject_draft_new" "false" "migration" ]
          [ "reject_vulnerabilities_zero_risk_new" "false" "migration" ]
          [ "remove_event_evidence" ]
          [ "remove_evidence" ]
          [ "remove_evidence_new" "false" "migration" ]
          [ "remove_files" ]
          [ "remove_finding" ]
          [ "remove_finding_new" "false" "migration" ]
          [ "remove_group" ]
          [ "remove_group_new" "false" "migration" ]
          [ "remove_group_tag" ]
          [ "remove_stakeholder_access" ]
          [ "remove_stakeholder_organization_access" ]
          [ "remove_tags" ]
          [ "remove_vulnerability" ]
          [ "remove_vulnerability_new" "false" "migration" ]
          [ "request_vulnerabilities_verification" ]
          [ "request_vulnerabilities_verification_new" "false" "migration" ]
          [ "request_vulnerabilities_zero_risk" ]
          [ "request_vulnerabilities_zero_risk_new" "false" "migration" ]
          [ "reset_expired_accepted_findings_new" "false" "migration" ]
          [ "resources" ]
          [ "sign_in" ]
          [ "solve_event" ]
          [ "stakeholder" ]
          [ "submit_draft" ]
          [ "submit_draft_new" "false" "migration" ]
          [ "submit_organization_finding_policy" "false" "migration" ]
          [ "subscribe_to_entity_report" "false" "migration" ]
          [ "toe_inputs" ]
          [ "toe_lines" ]
          [ "unsubscribe_from_group" ]
          [ "update_access_token" ]
          [ "update_event_evidence" ]
          [ "update_evidence" ]
          [ "update_evidence_description" ]
          [ "update_evidence_description_new" "false" "migration" ]
          [ "update_evidence_new" "false" "migration" ]
          [ "update_finding_description" ]
          [ "update_finding_description_new" "false" "migration" ]
          [ "update_forces_access_token" ]
          [ "update_group" ]
          [ "update_group_stakeholder" ]
          [ "update_organization_policies" ]
          [ "update_organization_stakeholder" ]
          [ "update_severity" ]
          [ "update_severity_new" "false" "migration" ]
          [ "update_toe_lines_sorts" ]
          [ "update_vulnerabilities_treatment_new" "false" "migration" ]
          [ "update_vulnerability_commit" ]
          [ "update_vulnerability_commit_new" "false" "migration" ]
          [ "update_vulnerability_treatment" ]
          [ "update_vulnerability_treatment_new" "false" "migration" ]
          [ "upload_file" ]
          [ "upload_file_new" "false" "migration" ]
          [ "verify_vulnerabilities_request" ]
          [ "verify_vulnerabilities_request_new" "false" "migration" ]
          [ "vulnerability" ]
          [ "vulnerability_new" "false" "migration" ]
        ])
      ++ [
        {
          output = "/integrates/linters/back/schema";
          gitlabExtra = gitlabLint;
        }
        {
          output = "/integrates/linters/charts";
          gitlabExtra = gitlabLint;
        }
        {
          output = "/integrates/web/e2e";
          gitlabExtra = gitlabPostDeployDev // {
            needs = [
              "integrates.back.deploy.dev"
              "integrates.front.deploy.dev"
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
