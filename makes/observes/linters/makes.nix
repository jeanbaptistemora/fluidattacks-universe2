{ inputs
, makeSearchPaths
, projectPath
, ...
}:
{
  lintPython = {
    imports = {
      observesArch = {
        config = "/observes/architecture/setup.imports.cfg";
        extraSources = [
          (makeSearchPaths {
            pythonPackage = builtins.map projectPath [
              "/observes/code_etl"
              "/observes/common/paginator"
              "/observes/common/singer_io"
              "/observes/common/utils_logger"
              "/observes/common/postgres_client"
              "/observes/services/batch_stability"
              "/observes/services/job_last_success"
              "/observes/services/jobs_scheduler"
              "/observes/services/migrate_tables"
              "/observes/services/timedoctor_tokens"
              "/observes/singer/streamer_dynamodb"
              "/observes/singer/streamer_zoho_crm"
              "/observes/singer/tap_bugsnag"
              "/observes/singer/tap_checkly"
              "/observes/singer/tap_csv"
              "/observes/singer/tap_delighted"
              "/observes/singer/tap_formstack"
              "/observes/singer/tap_git"
              "/observes/singer/tap_gitlab"
              "/observes/singer/tap_json"
              "/observes/singer/tap_mailchimp"
              "/observes/singer/tap_mixpanel"
              "/observes/singer/tap_timedoctor"
              "/observes/singer/tap_toe_files"
              "/observes/singer/tap_zoho_analytics"
              "/observes/singer/target_redshift"
            ];
          })
        ];
        src = "/observes/architecture";
      };
      observesTapCsv = {
        config = "/observes/singer/tap_csv/setup.imports.cfg";
        src = "/observes/singer/tap_csv";
      };
      observesTapFormstack = {
        config = "/observes/singer/tap_formstack/tap_formstack/setup.imports.cfg";
        src = "/observes/singer/tap_formstack";
      };
      observesTapGitlab = {
        config = "/observes/singer/tap_gitlab/tap_gitlab/setup.imports.cfg";
        src = "/observes/singer/tap_gitlab";
      };
      observesTapJson = {
        config = "/observes/singer/tap_json/tap_json/setup.imports.cfg";
        src = "/observes/singer/tap_json";
      };
      observesTapMailchimp = {
        config = "/observes/singer/tap_mailchimp/tap_mailchimp/setup.imports.cfg";
        src = "/observes/singer/tap_mailchimp";
      };
      observesTapMixpanel = {
        config = "/observes/singer/tap_mixpanel/tap_mixpanel/setup.imports.cfg";
        src = "/observes/singer/tap_mixpanel";
      };
      observesTapTimedoctor = {
        config = "/observes/singer/tap_timedoctor/tap_timedoctor/setup.imports.cfg";
        src = "/observes/singer/tap_timedoctor";
      };
      observesServiceTimedoctorTokens = {
        config = "/observes/services/timedoctor_tokens/timedoctor_tokens/setup.imports.cfg";
        src = "/observes/services/timedoctor_tokens";
      };
    };
    modules = {
      observesCodeEtl = {
        extraSources = [
          inputs.product.observes-env-code-etl-development
        ];
        python = "3.8";
        src = "/observes/code_etl/code_etl";
      };
      observesCodeEtlTests = {
        extraSources = [
          inputs.product.observes-env-code-etl-development
        ];
        python = "3.8";
        src = "/observes/code_etl/tests";
      };
      observesJobLastSuccess = {
        extraSources = [
          inputs.product.observes-env-job-last-success-runtime
        ];
        python = "3.8";
        src = "/observes/services/job_last_success/job_last_success";
      };
      observesJobLastSuccessTests = {
        extraSources = [
          inputs.product.observes-env-job-last-success-runtime
        ];
        python = "3.8";
        src = "/observes/services/job_last_success/tests";
      };
      observesServiceBatchStability = {
        extraSources = [
          inputs.product.observes-env-service-batch-stability-runtime
        ];
        python = "3.8";
        src = "/observes/services/batch_stability/batch_stability";
      };
      observesServiceJobsScheduler = {
        extraSources = [
          inputs.product.observes-env-service-jobs-scheduler-runtime
        ];
        python = "3.8";
        src = "/observes/services/jobs_scheduler/jobs_scheduler";
      };
      observesServiceMigrateTables = {
        extraSources = [
          inputs.product.observes-env-service-migrate-tables-runtime
        ];
        python = "3.8";
        src = "/observes/services/migrate_tables/migrate_tables";
      };
      observesStreamerZohoCrm = {
        extraSources = [
          inputs.product.observes-env-streamer-zoho-crm-runtime
        ];
        python = "3.8";
        src = "/observes/singer/streamer_zoho_crm/streamer_zoho_crm";
      };
      observesStreamerZohoCrmTests = {
        extraSources = [
          inputs.product.observes-env-streamer-zoho-crm-development
        ];
        python = "3.8";
        src = "/observes/singer/streamer_zoho_crm/tests";
      };
      observesTapCsv = {
        extraSources = [ inputs.product.observes-env-tap-csv-development ];
        python = "3.8";
        src = "/observes/singer/tap_csv/tap_csv";
      };
      observesTapCsvTests = {
        extraSources = [ inputs.product.observes-env-tap-csv-development ];
        python = "3.8";
        src = "/observes/singer/tap_csv/tests";
      };
      observesTapFormstack = {
        extraSources = [ inputs.product.observes-env-tap-formstack-runtime ];
        python = "3.8";
        src = "/observes/singer/tap_formstack/tap_formstack";
      };
      observesTapGitlab = {
        extraSources = [ inputs.product.observes-env-tap-gitlab-development ];
        python = "3.8";
        src = "/observes/singer/tap_gitlab/tap_gitlab";
      };
      observesTapGitlabTests = {
        extraSources = [ inputs.product.observes-env-tap-gitlab-development ];
        python = "3.8";
        src = "/observes/singer/tap_gitlab/tests";
      };
      observesTapJson = {
        extraSources = [ inputs.product.observes-env-tap-json-development ];
        python = "3.8";
        src = "/observes/singer/tap_json/tap_json";
      };
      observesTapMailchimp = {
        extraSources = [ inputs.product.observes-env-tap-mailchimp-development ];
        python = "3.8";
        src = "/observes/singer/tap_mailchimp/tap_mailchimp";
      };
      observesTapMailchimpTests = {
        extraSources = [ inputs.product.observes-env-tap-mailchimp-development ];
        python = "3.8";
        src = "/observes/singer/tap_mailchimp/tests";
      };
      observesTapMixpanel = {
        extraSources = [ inputs.product.observes-env-tap-mixpanel-development ];
        python = "3.8";
        src = "/observes/singer/tap_mixpanel/tap_mixpanel";
      };
      observesTapMixpanelTests = {
        extraSources = [ inputs.product.observes-env-tap-mixpanel-development ];
        python = "3.8";
        src = "/observes/singer/tap_mixpanel/tests";
      };
      observesTapTimedoctor = {
        extraSources = [ inputs.product.observes-env-tap-timedoctor-runtime ];
        python = "3.8";
        src = "/observes/singer/tap_timedoctor/tap_timedoctor";
      };
      observesTargetRedshift = {
        extraSources = [
          inputs.product.observes-env-target-redshift-runtime
        ];
        python = "3.8";
        src = "/observes/singer/target_redshift/target_redshift";
      };
      observesServiceTimedoctorTokens = {
        extraSources = [
          inputs.product.observes-env-service-timedoctor-tokens-runtime
        ];
        python = "3.8";
        src = "/observes/services/timedoctor_tokens/timedoctor_tokens";
      };
    };
  };
}
