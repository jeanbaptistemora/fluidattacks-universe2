{ inputs
, makeSearchPaths
, outputs
, projectPath
, ...
}:
{
  lintPython = {
    imports = {
      observesArch = {
        config = "/observes/architecture/setup.imports.cfg";
        searchPaths.source = [
          (makeSearchPaths {
            pythonPackage = builtins.map projectPath [
              "/observes/code_etl"
              "/observes/common/paginator"
              "/observes/common/singer_io"
              "/observes/common/utils_logger"
              "/observes/common/postgres_client"
              "/observes/common/purity"
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
      observesCommonPaginator = {
        config = "/observes/common/paginator/paginator/setup.imports.cfg";
        src = "/observes/common/paginator";
      };
      observesCommonPostgresClient = {
        config = "/observes/common/postgres_client/postgres_client/setup.imports.cfg";
        src = "/observes/common/postgres_client";
      };
      observesCommonPurity = {
        config = "/observes/common/purity/purity/setup.imports.cfg";
        src = "/observes/common/purity";
      };
      observesCommonSingerIo = {
        config = "/observes/common/singer_io/singer_io/setup.imports.cfg";
        src = "/observes/common/singer_io";
      };
      observesTapAnnounceKit = {
        config = "${inputs.observesIndex.tap.announcekit.src}/setup.imports.cfg";
        src = inputs.observesIndex.tap.announcekit.root;
      };
      observesTapBugsnag = {
        config = "${inputs.observesIndex.tap.bugsnag.src}/setup.imports.cfg";
        src = inputs.observesIndex.tap.bugsnag.root;
      };
      observesTapCheckly = {
        config = "${inputs.observesIndex.tap.checkly.src}/setup.imports.cfg";
        src = inputs.observesIndex.tap.checkly.root;
      };
      observesTapCsv = {
        config = "${inputs.observesIndex.tap.csv.src}/setup.imports.cfg";
        src = inputs.observesIndex.tap.csv.root;
      };
      observesTapDelighted = {
        config = "${inputs.observesIndex.tap.delighted.src}/setup.imports.cfg";
        src = inputs.observesIndex.tap.delighted.root;
      };
      observesTapFormstack = {
        config = "${inputs.observesIndex.tap.formstack.src}/setup.imports.cfg";
        src = inputs.observesIndex.tap.formstack.root;
      };
      observesTapGitlab = {
        config = "${inputs.observesIndex.tap.gitlab.src}/setup.imports.cfg";
        src = inputs.observesIndex.tap.gitlab.root;
      };
      observesTapJson = {
        config = "${inputs.observesIndex.tap.json.src}/setup.imports.cfg";
        src = inputs.observesIndex.tap.json.root;
      };
      observesTapMailchimp = {
        config = "${inputs.observesIndex.tap.mailchimp.src}/setup.imports.cfg";
        src = inputs.observesIndex.tap.mailchimp.root;
      };
      observesTapMixpanel = {
        config = "${inputs.observesIndex.tap.mixpanel.src}/setup.imports.cfg";
        src = inputs.observesIndex.tap.mixpanel.root;
      };
      observesTapTimedoctor = {
        config = "${inputs.observesIndex.tap.timedoctor.src}/setup.imports.cfg";
        src = inputs.observesIndex.tap.timedoctor.root;
      };
      observesServiceTimedoctorTokens = {
        config = "/observes/services/timedoctor_tokens/timedoctor_tokens/setup.imports.cfg";
        src = "/observes/services/timedoctor_tokens";
      };
    };
    modules = {
      observesCodeEtl = {
        searchPaths.source = [
          outputs."/observes/etl/code/env/development"
        ];
        python = "3.8";
        src = "/observes/code_etl/code_etl";
      };
      observesCodeEtlTests = {
        searchPaths.source = [
          outputs."/observes/etl/code/env/development"
        ];
        python = "3.8";
        src = "/observes/code_etl/tests";
      };
      observesCommonPaginator = {
        searchPaths.source = [
          outputs."/observes/common/paginator/env/development"
        ];
        python = "3.8";
        src = "/observes/common/paginator/paginator";
      };
      observesCommonPostgresClient = {
        searchPaths.source = [
          outputs."/observes/common/postgres-client/env/development"
        ];
        python = "3.8";
        src = "/observes/common/postgres_client/postgres_client";
      };
      observesCommonPurity = {
        searchPaths.source = [
          outputs."/observes/common/purity/env/runtime"
        ];
        python = "3.8";
        src = "/observes/common/purity/purity";
      };
      observesCommonPurityTests = {
        searchPaths.source = [
          outputs."/observes/common/purity/env/runtime"
        ];
        python = "3.8";
        src = "/observes/common/purity/tests";
      };
      observesCommonPostgresClientTests = {
        searchPaths.source = [
          outputs."/observes/common/postgres-client/env/development"
        ];
        python = "3.8";
        src = "/observes/common/postgres_client/postgres_client";
      };
      observesCommonSingerIo = {
        searchPaths.source = [
          outputs."/observes/common/singer-io/env/development"
        ];
        python = "3.8";
        src = "/observes/common/singer_io/singer_io";
      };
      observesCommonSingerIoTests = {
        searchPaths.source = [
          outputs."/observes/common/singer-io/env/development"
        ];
        python = "3.8";
        src = "/observes/common/singer_io/tests";
      };
      observesJobLastSuccess = {
        searchPaths.source = [
          outputs."/observes/service/job-last-success/env/runtime"
        ];
        python = "3.8";
        src = "/observes/services/job_last_success/job_last_success";
      };
      observesJobLastSuccessTests = {
        searchPaths.source = [
          outputs."/observes/service/job-last-success/env/runtime"
        ];
        python = "3.8";
        src = "/observes/services/job_last_success/tests";
      };
      observesServiceBatchStability = {
        searchPaths.source = [
          outputs."/observes/service/batch-stability/env/runtime"
        ];
        python = "3.8";
        src = "/observes/services/batch_stability/batch_stability";
      };
      observesServiceJobsScheduler = {
        searchPaths.source = [
          outputs."/observes/service/jobs-scheduler/env/runtime"
        ];
        python = "3.8";
        src = "/observes/services/jobs_scheduler/jobs_scheduler";
      };
      observesServiceMigrateTables = {
        searchPaths.source = [
          outputs."/observes/service/migrate-tables/env/runtime"
        ];
        python = "3.8";
        src = "/observes/services/migrate_tables/migrate_tables";
      };
      observesStreamerZohoCrm = {
        searchPaths.source = [
          outputs."${inputs.observesIndex.tap.zoho_crm.env.runtime}"
        ];
        python = "3.8";
        src = inputs.observesIndex.tap.zoho_crm.src;
      };
      observesStreamerZohoCrmTests = {
        searchPaths.source = [
          outputs."${inputs.observesIndex.tap.zoho_crm.env.dev}"
        ];
        python = "3.8";
        src = inputs.observesIndex.tap.zoho_crm.tests;
      };
      observesTapAnnounceKit = {
        searchPaths.source = [
          outputs."${inputs.observesIndex.tap.announcekit.env.runtime}"
        ];
        python = "3.8";
        src = inputs.observesIndex.tap.announcekit.src;
      };
      observesTapAnnounceKitTests = {
        searchPaths.source = [
          outputs."/observes/singer/tap-announcekit/env/development"
        ];
        python = "3.8";
        src = inputs.observesIndex.tap.announcekit.tests;
      };
      observesTapBugsnag = {
        searchPaths.source = [
          outputs."${inputs.observesIndex.tap.bugsnag.env.runtime}"
        ];
        python = "3.8";
        src = inputs.observesIndex.tap.bugsnag.src;
      };
      observesTapCheckly = {
        searchPaths.source = [
          outputs."${inputs.observesIndex.tap.checkly.env.runtime}"
        ];
        python = "3.8";
        src = inputs.observesIndex.tap.checkly.src;
      };
      observesTapCsv = {
        searchPaths.source = [
          outputs."${inputs.observesIndex.tap.csv.env.dev}"
        ];
        python = "3.8";
        src = inputs.observesIndex.tap.csv.src;
      };
      observesTapCsvTests = {
        searchPaths.source = [
          outputs."${inputs.observesIndex.tap.csv.env.dev}"
        ];
        python = "3.8";
        src = inputs.observesIndex.tap.csv.tests;
      };
      observesTapDelighted = {
        searchPaths.source = [
          outputs."${inputs.observesIndex.tap.delighted.env.runtime}"
        ];
        python = "3.8";
        src = inputs.observesIndex.tap.delighted.src;
      };
      observesTapDynamo = {
        searchPaths.source = [
          outputs."${inputs.observesIndex.tap.dynamo.env.runtime}"
        ];
        python = "3.8";
        src = inputs.observesIndex.tap.dynamo.src;
      };
      observesTapFormstack = {
        searchPaths.source = [
          outputs."${inputs.observesIndex.tap.formstack.env.runtime}"
        ];
        python = "3.8";
        src = inputs.observesIndex.tap.formstack.src;
      };
      observesTapGitlab = {
        searchPaths.source = [
          outputs."${inputs.observesIndex.tap.gitlab.env.dev}"
        ];
        python = "3.8";
        src = inputs.observesIndex.tap.gitlab.src;
      };
      observesTapGitlabTests = {
        searchPaths.source = [
          outputs."${inputs.observesIndex.tap.gitlab.env.dev}"
        ];
        python = "3.8";
        src = inputs.observesIndex.tap.gitlab.tests;
      };
      observesTapJson = {
        searchPaths.source = [
          outputs."${inputs.observesIndex.tap.json.env.dev}"
        ];
        python = "3.8";
        src = inputs.observesIndex.tap.json.src;
      };
      observesTapMailchimp = {
        searchPaths.source = [
          outputs."${inputs.observesIndex.tap.mailchimp.env.dev}"
        ];
        python = "3.8";
        src = inputs.observesIndex.tap.mailchimp.src;
      };
      observesTapMailchimpTests = {
        searchPaths.source = [
          outputs."${inputs.observesIndex.tap.mailchimp.env.dev}"
        ];
        python = "3.8";
        src = inputs.observesIndex.tap.mailchimp.tests;
      };
      observesTapMixpanel = {
        searchPaths.source = [
          outputs."${inputs.observesIndex.tap.mixpanel.env.dev}"
        ];
        python = "3.8";
        src = inputs.observesIndex.tap.mixpanel.src;
      };
      observesTapMixpanelTests = {
        searchPaths.source = [
          outputs."${inputs.observesIndex.tap.mixpanel.env.dev}"
        ];
        python = "3.8";
        src = inputs.observesIndex.tap.mixpanel.tests;
      };
      observesTapTimedoctor = {
        searchPaths.source = [
          outputs."${inputs.observesIndex.tap.timedoctor.env.runtime}"
        ];
        python = "3.8";
        src = inputs.observesIndex.tap.timedoctor.src;
      };
      observesTargetRedshift = {
        searchPaths.source = [
          outputs."${inputs.observesIndex.target.redshift.env.runtime}"
        ];
        python = "3.8";
        src = inputs.observesIndex.target.redshift.src;
      };
      observesServiceTimedoctorTokens = {
        searchPaths.source = [
          outputs."/observes/service/timedoctor-tokens/env/runtime"
        ];
        python = "3.8";
        src = "/observes/services/timedoctor_tokens/timedoctor_tokens";
      };
    };
  };
}
